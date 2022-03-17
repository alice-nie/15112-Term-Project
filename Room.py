# ABOUT this file: draws the room and handles switching omniBox modes

from cmu_112_graphics import *
# following cmu 112 graphic framework
from Calendar import *
from OmniBox import *
from StatBars import *
from DatingSim import *

# any quirky color names from http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
# all images drawn by Nhu Tat



class Room(Mode):
    
    # code for the following two functions taken from https://www.cs.cmu.edu/~112/notes/notes-graphics.html
    def getCellBounds(self, row, col):
        x0 = 0 + (col * self.quadWidth)
        y0 = 0 + (row * self.quadHeight)
        x1 = x0 + self.quadWidth
        y1 = y0 + self.quadHeight
        return (x0, y0, x1, y1)


    def getCell(self, x, y):
        row = int(y / self.quadHeight)
        col = int(x / self.quadWidth)
        return (row, col)

    # initializes variables
    def appStarted(self):

        self.viewCalendar = False
        self.app.calendar.appStarted()

        self.app.omniBox.appStarted()

        self.app.statBars.appStarted()

        self.viewQuest = False
        self.app.quest.appStarted()


        self.playerSprite()
        self.background()
        self.buttons()

        # for JSON stuff
        self.inputtedValue = ''
        self.intro = True
        self.mouseOverInputArea = False
        self.clickedOnInputArea = False
        self.mouseOverYes = self.mouseOverNo = False
        self.recurringPlayer = False
        self.newPlayer = False
        self.welcome = False
        self.mouseOverContinue = self.mouseOverNewGame = False
        self.mouseOverOk = False
    
    # initializes variables for the room
    def background(self):

        self.barBoxTop = self.height - (self.incrementY//2)- 10


        self.roomPlain = self.loadImage('roomPlain.png')
        self.roomBed = self.loadImage('roomBed.png')
        self.roomDoor = self.loadImage('roomDoor.png')
        self.roomFood = self.loadImage('roomFood.png')
        self.roomWork = self.loadImage('roomWork.png')
        self.currentRoomState = self.roomPlain

        # split room into Quadrants:
        self.roomRows = self.roomCols = 2

        self.quadWidth = self.width // self.roomCols
        self.quadHeight = self.height // self.roomRows
        
        self.quadrant1 = (0, 1)
        self.quadrant2 = (0, 0)
        self.quadrant3 = (1, 0)
        self.quadrant4 = (1, 1)
        self.inQuad = None

    # intializes variables for the player's sprite 
    def playerSprite(self):
        # following code from https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html
        # playerSpriteSheet image drawn by Nhu Tat, reference pic: https://www.google.com/imgres?imgurl=https://theresahanson.com/images/uploads/walkingsprite.jpg&imgrefurl=https://theresahanson.com/work/show/walking-sprite&tbnid=tMaY3QGX-0DXzM&vet=1&docid=zrs2J3TxtI854M&w=1296&h=721&hl=en-US&source=sh/x/im
        playerSpriteSheet = self.loadImage('playerSpriteSheet.png')
        self.resizedPlayerSpriteSheet = self.scaleImage(playerSpriteSheet, 3/4) 
        playerSheetWidth, playerSheetHeight = self.resizedPlayerSpriteSheet.size
        self.incrementX = playerSheetWidth / 9
        self.incrementY = playerSheetHeight / 4
        incrementX, incrementY = self.incrementX, self.incrementY

        x0, y0 = 0, 0
        x1, y1 = x0 + incrementX, y0 + incrementY
 
        self.playerWalkingRight = [ ]
        self.playerWalkingLeft = [ ]
        self.playerWalkingForward = [ ]
        self.playerWalkingBack = [ ]
        playerMovement = [self.playerWalkingRight, self.playerWalkingLeft, self.playerWalkingForward, self.playerWalkingBack]


        # create sprite list for each type of movement
        for move in range(4):
            # increment from base
            y3 = y0 + move*incrementY
            y4 = y1 + move*incrementY
            if move == 1: # read right to left
                x0 = 8*incrementX
                x1 = x0 + incrementX
                incrementX *= -1
            else: # read left to right
                incrementX = abs(incrementX)
                x0 = 0
                x1 = x0 + incrementX
            for i in range(9):
                spriteSequence = self.resizedPlayerSpriteSheet.crop((x0 + i*incrementX, y3, x1 + i*incrementX, y4))
                playerMovement[move].append(spriteSequence)    

        self.playerSpriteCounter = 0
        self.playerLocation = [self.width//2, self.height//2]
        self.currentPlayerSprite = self.playerWalkingForward[0]
        

    # intializes any button-like variables
    def buttons(self):
        self.br = 15
        healthBoxTop = self.barBoxTop
        self.mouseInQuest = False
        self.qbX, self.qbY = self.width//18, healthBoxTop  - 3*(self.app.calendar.cellHeight//2)
        self.mouseInCalendar = False
        self.cbX, self.cbY = self.width//18, healthBoxTop  - 2*(self.app.calendar.cellHeight//2)
        self.mouseInHelp = False
        self.viewHelp = False
        self.hbX, self.hbY = self.width//18, healthBoxTop  - self.app.calendar.cellHeight//2
        self.showWarning = False

###############################################################################

    # distance formula
    def distance(self, x0, y0, x1, y1):
        return ((x0 - x1) ** 2 + (y0 - y1) ** 2) ** 0.5

    # tracks mouse movement
    def mouseMoved(self, event):

        # intro
        if self.intro:
            if self.distance(event.x, event.y, self.width//2 , self.height//2 + self.incrementY//6) <= 30: # radius of notice used in omniBox
                self.mouseOverInputArea = True
            else: self.mouseOverInputArea = False
            if self.inputtedValue != '':
                if self.distance(event.x, event.y, self.width//2 - self.incrementX, self.height//2 + self.incrementY//2) <= 30:
                    self.mouseOverYes = True
                else: self.mouseOverYes = False
                if self.distance(event.x, event.y, self.width//2 + self.incrementX, self.height//2 + self.incrementY//2) <= 30:
                    self.mouseOverNo = True
                else: self.mouseOverNo = False

        # welcome
        if self.welcome and self.recurringPlayer:
            if self.distance(event.x, event.y, self.width//2 - self.incrementX, self.height//2 + self.incrementY//2) <= 30:
                self.mouseOverContinue = True
            else: self.mouseOverContinue = False
            if self.distance(event.x, event.y, self.width//2 + self.incrementX, self.height//2 + self.incrementY//2) <= 30:
                self.mouseOverNewGame = True
            else: self.mouseOverNewGame = False
        elif self.welcome and self.newPlayer:
            if self.distance(event.x, event.y, self.width//2, self.height//2 + self.incrementY//2) <= 30:
                self.mouseOverOk = True
            else: self.mouseOverOk = False
            


        if self.viewCalendar == True:
            self.app.calendar.mouseMoved(event)
        
        self.app.omniBox.mouseMoved(event)

        # buttons
        if self.distance(event.x, event.y, self.qbX, self.qbY) <= self.br:
            self.mouseInQuest = True
        else: self.mouseInQuest = False

        if self.distance(event.x, event.y, self.cbX, self.cbY) <= self.br:
            self.mouseInCalendar = True
        else: self.mouseInCalendar = False

        if self.distance(event.x, event.y, self.hbX, self.hbY) <= self.br:
            self.mouseInHelp = True
        else: self.mouseInHelp = False

    # tracks mouse pressed
    def mousePressed(self, event):

        # intro
        if self.mouseOverInputArea:
            self.clickedOnInputArea = True
        elif self.mouseOverYes:
            if self.inputtedValue in char.player.progress:
                self.welcome, self.intro = True, False
                self.recurringPlayer = True
                self.intro = False
            else: 
                self.welcome, self.intro = True, False
                self.newPlayer = True
                char.player.currentPlayer = self.inputtedValue
                char.player.progress[char.player.currentPlayer] = dict()
                # intialize (updates in dating sim classes when time changes)
                listOfStatKeys = ['health', 'stress', 'productivity', 'sleep', 'meals', 'currentHour', 'currentMinute', 'currentDay', 'currentMonth', 'currentWeek',
                                'daysProductivity', 'daysSleep', 'daysMeals', 'daysFun', 'timeBlocks']
                listOfStats = [char.player.health, char.player.stress, char.player.productivity, char.player.sleep, char.player.meals, char.player.currentHour, 
                                    char.player.currentMinute, char.player.currentDay, char.player.currentMonth, char.player.currentWeek, char.player.daysProductivity,
                                    char.player.daysSleep, char.player.daysMeals, char.player.daysFun, char.player.timeBlocks]
                for i in range(len(listOfStats)):
                    char.player.progress[char.player.currentPlayer]['char.player.' + listOfStatKeys[i]] = listOfStats[i]
            self.clickedOnInputArea = False

        elif self.mouseOverNo:
            self.inputtedValue = '___'
            self.clickedOnInputArea = False

        # welcome
        if self.mouseOverContinue:
            char.player.currentPlayer = self.inputtedValue
        
            # revert
            progress = char.player.progress[char.player.currentPlayer]
            loadOldStats = [progress['char.player.health'], progress['char.player.stress'], progress['char.player.productivity'], progress['char.player.sleep'],
                            progress['char.player.meals'], progress['char.player.currentHour'], progress['char.player.currentMinute'], progress['char.player.currentDay'],
                            progress['char.player.currentMonth'], progress['char.player.currentWeek'], progress['char.player.daysProductivity'], progress['char.player.daysSleep'],
                            progress['char.player.daysMeals'], progress['char.player.daysFun'], progress['char.player.timeBlocks']]

            [char.player.health, char.player.stress, char.player.productivity, char.player.sleep, char.player.meals, char.player.currentHour, 
            char.player.currentMinute, char.player.currentDay, char.player.currentMonth, char.player.currentWeek, char.player.daysProductivity,
            char.player.daysSleep, char.player.daysMeals, char.player.daysFun, char.player.timeBlocks] = loadOldStats

            self.welcome = False

        elif self.mouseOverNewGame:
            char.player.currentPlayer = self.inputtedValue
            listOfStatKeys = ['health', 'stress', 'productivity', 'sleep', 'meals', 'currentHour', 'currentMinute', 'currentDay', 'currentMonth', 'currentWeek',
                                'daysProductivity', 'daysSleep', 'daysMeals', 'daysFun', 'timeBlocks']
            listOfStats = [char.player.health, char.player.stress, char.player.productivity, char.player.sleep, char.player.meals, char.player.currentHour, 
                                char.player.currentMinute, char.player.currentDay, char.player.currentMonth, char.player.currentWeek, char.player.daysProductivity,
                                char.player.daysSleep, char.player.daysMeals, char.player.daysFun, char.player.timeBlocks]
            for i in range(len(listOfStatKeys)):
                char.player.progress[char.player.currentPlayer]['char.player.' + listOfStatKeys[i]] = listOfStats[i]
            self.welcome = False

        elif self.mouseOverOk:
            self.welcome = False

        # calendar
        if self.viewCalendar == True:
            self.app.calendar.mousePressed(event)


        self.app.omniBox.mousePressed(event)

        
        if self.app.omniBox.mouseOverClass:
            self.app.setActiveMode(self.app.datingSim)
            self.app.omniBox.mouseOverClass = False
            
            # check which classes are available
        
            if char.player.currentDay in self.app.calendar.listOfMonthEvents[char.player.currentMonth]:
                for course in self.app.calendar.listOfMonthEvents[char.player.currentMonth][char.player.currentDay]:
                    listOfInfo = self.app.calendar.classes[course]
                    beginningTime = listOfInfo[0]
                    beginningHour, beginningMinute = (beginningTime//100) % 100, beginningTime % 100
                    endTime = listOfInfo[1]
                    endHour, endMinute = (endTime//100) % 100, endTime % 100
                    if char.player.currentHour == beginningHour and char.player.currentMinute == beginningMinute:
                        if 'Programming Lecture' in course: char.Cs15112.classTime = True
                        elif 'Programming Recitation' in course: char.Cs15112.recitation = True
                        elif 'Programming Collab' in course: char.Cs15112.collab = True
                        elif 'Microecon' in course: char.Microecon.classTime = True
                        elif 'Calc' in course: char.Calc.classTime = True
                        elif 'Interp' in course: char.Interp.classTime = True
                        elif 'Science' in course: char.BS.classTime = True
                    if (char.player.currentHour == beginningHour and 
                        beginningMinute < char.player.currentMinute < 60): # some classes, after some time you can't even join tardy, must be within the hour
                        if 'Programming Lecture' in course: char.Cs15112.classTimeTardy = True
                        elif 'Programming Recitation' in course: char.Cs15112.recitation = True
                        elif 'Microecon' in course: char.Microecon.classTimeTardy = True
                        elif 'Calc' in course: char.Calc.classTimeTardy = True
                        elif 'Interp' in course: char.Interp.classTimeTardy = True
                        elif 'Science' in course: char.BS.classTimeTardy = True

        


        # buttons
        if self.mouseInCalendar:
            self.viewCalendar = True
        elif (self.mouseInCalendar == False and not
            ((self.app.calendar.calX0 <= event.x <= self.app.calendar.calX1) and
            (0 <= event.y <= self.app.calendar.calY1))):
            self.viewCalendar = False


        spacingX = (self.app.calendar.calX1 - self.app.calendar.calX0) // 7
        spacingY = (self.app.calendar.calY1 - self.app.calendar.calY0) // 5        
        if self.mouseInHelp:
            self.viewHelp = True
        elif (self.mouseInCalendar == False and not
            ((self.width//2 - (2*spacingX) <= event.x <= self.width//2 + (2*spacingX)) and
            (self.height//2 - (1.5*spacingY) <= event.y <= self.height//2 + (1.5*spacingY)))):
            self.viewHelp = False

        spacingX = self.width//5
        spacingY = self.height//6
        x0, y0 = self.width//2 - spacingX, self.height//2 - 1.5*spacingY
        x1, y1 = self.width//2 + spacingX, self.height//2 + 1.5*spacingY
        if self.mouseInQuest:
            self.app.quest.bestCourseOfAction()
            self.viewQuest = True
        elif (self.mouseInCalendar == False and not
            (x0 <= event.x <= x1 and y0 <= event.y <= y1)):
            self.viewQuest = False


    # pressing certain keys may trigger certain actions
    def keyPressed(self, event):

        # intro
        if self.clickedOnInputArea:
            if event.key == 'Space': self.inputtedValue += ' '
            elif event.key == 'Delete': self.inputtedValue = self.inputtedValue[:len(self.inputtedValue) - 1]
            else: self.inputtedValue += str(event.key)
            

        self.app.omniBox.keyPressed(event)
        
        # moving sprite
        if (event.key == 'w' or event.key == 'a' or event.key == 's' or event.key == 'd') and not self.intro and not self.welcome:
            
            # spriteCounter code taken from https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html#spritesheetsWithCropping
            self.playerSpriteCounter = (1 + self.playerSpriteCounter) % len(self.playerWalkingLeft)
            dx = 25
            dy = 20
            
            if event.key == 'a':
                self.currentPlayerSprite = self.playerWalkingLeft[self.playerSpriteCounter]
                self.playerLocation[0] -= dx
                if self.playerMoveIsLegal() == False:
                    self.playerLocation[0] += dx

            elif event.key == 'd':
                self.currentPlayerSprite = self.playerWalkingRight[self.playerSpriteCounter]
                self.playerLocation[0] += dx
                if self.playerMoveIsLegal() == False:
                    self.playerLocation[0] -= dx

            elif event.key == 'w':
                self.currentPlayerSprite = self.playerWalkingBack[self.playerSpriteCounter]
                self.playerLocation[1] -= dy
                if self.playerMoveIsLegal() == False:
                    self.playerLocation[1] += dy

            elif event.key == 's':
                self.currentPlayerSprite = self.playerWalkingForward[self.playerSpriteCounter]
                self.playerLocation[1] += dy
                if self.playerMoveIsLegal() == False:
                    self.playerLocation[1] -= dy
            
            # keeps track of player's quadrant
            playerRow, playerCol = self.getCell(self.playerLocation[0], self.playerLocation[1])
            for quadrant in [self.quadrant1, self.quadrant2, self.quadrant3, self.quadrant4]:
                quadRow, quadCol = quadrant
                if (playerRow, playerCol) == (quadRow, quadCol):
                    self.inQuad = quadrant

            # check for roomState
            quadrantHeight, quadrantWidth = self.height//2, self.width//2          
            if self.inQuad == self.quadrant1:
                #row, col = self.quadrant1
                #x0, y0, x1, y1 = self.getCellBounds(row, col)
                if self.playerLocation[1] <= 2*(quadrantHeight//3):
                    self.currentRoomState = self.roomBed
                else:
                    self.currentRoomState = self.roomPlain
            elif self.inQuad == self.quadrant2:
                #row, col = self.quadrant2
                #x0, y0, x1, y1 = self.getCellBounds(row, col)
                if self.playerLocation[1] <= quadrantHeight//2:
                    self.currentRoomState = self.roomWork
                elif self.playerLocation[1] >= quadrantHeight//2 and (self.playerLocation[0] <= quadrantWidth//2):
                    self.currentRoomState = self.roomFood
                else:
                    self.currentRoomState = self.roomPlain
            elif self.inQuad == self.quadrant3:
                #row, col = self.quadrant3
                #x0, y0, x1, y1 = self.getCellBounds(row, col)
                if self.playerLocation[0] >= quadrantWidth//3:
                    self.currentRoomState = self.roomDoor
                elif self.playerLocation[0] <= quadrantWidth//3:
                    self.currentRoomState = self.roomFood
            else:
                self.currentRoomState = self.roomPlain

            # change modes in the omniBox
            if self.currentRoomState == self.roomBed:
                self.app.omniBox.sleepMode = True
                self.app.omniBox.eatMode = self.app.omniBox.outsideMode = self.app.omniBox.studyOrClassMode = False
                self.app.omniBox.studyMode = self.app.omniBox.studyPage = self.app.omniBox.studyBS = self.app.omniBox.studyMicroecon = self.app.omniBox.study15112 = self.app.omniBox.studyCalc = self.app.omniBox.studyInterp = False
                self.app.omniBox.inputtedValue = '___'
            elif self.currentRoomState == self.roomFood:
                self.app.omniBox.eatMode = True
                self.app.omniBox.sleepMode = self.app.omniBox.outsideMode = self.app.omniBox.studyOrClassMode = False
                self.app.omniBox.studyMode = self.app.omniBox.studyPage = self.app.omniBox.studyBS = self.app.omniBox.studyMicroecon = self.app.omniBox.study15112 = self.app.omniBox.studyCalc = self.app.omniBox.studyInterp = False
                self.app.omniBox.inputtedValue = '___'
            elif self.currentRoomState == self.roomDoor:
                self.app.omniBox.outsideMode = True
                self.app.omniBox.sleepMode = self.app.omniBox.eatMode = self.app.omniBox.studyOrClassMode = False
                self.app.omniBox.studyMode = self.app.omniBox.studyPage = self.app.omniBox.studyBS = self.app.omniBox.studyMicroecon = self.app.omniBox.study15112 = self.app.omniBox.studyCalc = self.app.omniBox.studyInterp = False
                self.app.omniBox.inputtedValue = '___'
            elif self.currentRoomState == self.roomWork:
                self.app.omniBox.studyOrClassMode = True
                self.app.omniBox.sleepMode = self.app.omniBox.eatMode = self.app.omniBox.outsideMode = False
                self.app.omniBox.studyMode = self.app.omniBox.studyPage = self.app.omniBox.studyBS = self.app.omniBox.studyMicroecon = self.app.omniBox.study15112 = self.app.omniBox.studyCalc = self.app.omniBox.studyInterp = False
                self.app.omniBox.inputtedValue = '___'
            else:
                self.app.omniBox.sleepMode = self.app.omniBox.eatMode = self.app.omniBox.outsideMode = self.app.omniBox.currentRoomState = False
                self.app.omniBox.studyMode = self.app.omniBox.studyPage = self.app.omniBox.studyBS = self.app.omniBox.studyMicroecon = self.app.omniBox.study15112 = self.app.omniBox.studyCalc = self.app.omniBox.studyInterp = False
                self.app.omniBox.inputtedValue = '___'

            if self.app.omniBox.sleepMode or self.app.omniBox.eatMode or self.app.omniBox.outsideMode or self.app.omniBox.studyOrClassMode:
                self.app.omniBox.shopMode = self.app.omniBox.statsMode = self.app.omniBox.studyBS = self.app.omniBox.studyMicroecon = self.app.omniBox.study15112 = self.app.omniBox.studyCalc = self.app.omniBox.studyInterp = self.studyMode = self.studyPage =  False

            elif self.app.omniBox.shopMode or self.app.omniBox.statsMode:
                self.app.omniBox.sleepMode = self.app.omniBox.eatMode = self.app.omniBox.outsideMode = self.app.omniBox.studyOrClassMode = self.app.omniBox.studyBS = self.app.omniBox.studyMicroecon = self.app.omniBox.study15112 = self.app.omniBox.studyCalc = self.app.omniBox.studyInterp = False
            
            
    # returns True if player is within the bounds of the game
    def playerMoveIsLegal(self):
        x, y = self.playerLocation
        portionOfSpriteWidth = self.incrementX * (2/5)
        portionOfSpriteHeight = self.incrementY * (2/5)
        if ((0 + portionOfSpriteWidth <= x < self.width - portionOfSpriteWidth) and
            (0 + portionOfSpriteHeight <= y < self.barBoxTop - portionOfSpriteHeight)):
            return True
        return False


    # code taken from https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html
    def getCachedPhotoImage(self, image):
        # stores a cached version of the PhotoImage in the PIL/Pillow image
        if ('cachedPhotoImage' not in image.__dict__):
            image.cachedPhotoImage = ImageTk.PhotoImage(image)
        return image.cachedPhotoImage

    


###############################################################################


    # draws everything
    def redrawAll(self, canvas):

        self.drawRoom(canvas)
        self.drawPlayer(canvas)
        self.drawButtons(canvas)
        
        self.app.omniBox.redrawAll(canvas)

        self.app.statBars.redrawAll(canvas)
        
        if self.viewHelp == True:
            self.drawHelpPopUp(canvas)

        if self.viewCalendar == True:
            self.app.calendar.redrawAll(canvas)

        if self.viewQuest == True:
            self.app.quest.redrawAll(canvas)

        if self.intro:
            self.drawIntro(canvas)

        if self.welcome:
            self.drawWelcome(canvas)

       
    # draws the different room states
    # following code from https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html
    def drawRoom(self, canvas):
        photoImage = self.getCachedPhotoImage(self.currentRoomState)
        canvas.create_image(self.width//2, self.height//2, image = photoImage)

    # draws the player's sprite
    def drawPlayer(self, canvas):
        x, y = self.playerLocation
        sprite = self.getCachedPhotoImage(self.currentPlayerSprite)
        canvas.create_image(x, y, image = sprite)

    # draws the Quest, Calendar, and Help Button
    def drawButtons(self, canvas):
        qr = cr = hr = self.br
        qTextSize = cTextSize = hTextSize = 18
        qFill = cFill = hFill = ''
        qWidth = cWidth = hWidth = 3
        if self.mouseInQuest:
            qr, qTestSize, qFill, qWidth = self.br + 5, 20, 'mistyrose', 5
        if self.mouseInCalendar:
            cr, cTextSize, cFill, cWidth = self.br + 5, 20, 'mistyrose', 5
        if self.mouseInHelp:
            hr, hTextSize, hFill, hWidth = self.br + 5, 20, 'mistyrose', 5
        


        canvas.create_oval(self.qbX - qr, self.qbY - qr, self.qbX + qr, self.qbY + qr, outline = 'gray', width = qWidth, fill = qFill)
        canvas.create_text(self.qbX, self.qbY, text = 'Q', font = f'Courier {qTextSize} bold', fill = 'gray')
        canvas.create_oval(self.cbX - cr, self.cbY - cr, self.cbX + cr, self.cbY + cr, outline = 'gray', width = cWidth, fill = cFill)
        canvas.create_text(self.cbX, self.cbY, text = 'C', font = f'Courier {cTextSize} bold', fill = 'gray')
        canvas.create_oval(self.hbX - hr, self.hbY - hr, self.hbX + hr, self.hbY + hr, outline = 'gray', width = hWidth, fill = hFill)
        canvas.create_text(self.hbX, self.hbY, text = '?', font = f'Courier {hTextSize} bold', fill = 'gray')

    # draws the help popup
    def drawHelpPopUp(self, canvas):
        spacingX = (self.app.calendar.calX1 - self.app.calendar.calX0) // 7
        spacingY = (self.app.calendar.calY1 - self.app.calendar.calY0) // 5
        x0, y0, x1, y1 = self.width//2 - (2*spacingX), self.height//2 - (1.5*spacingY), self.width//2 + (2*spacingX), self.height//2 + (1.5*spacingY)

        self.app.calendar.drawRoundedRectangle(canvas, x0, y0, x1, y1, 20, 'navajo white', 'gray', 5)

        
        text = 'There is no help :)'
        midX, midY = (x0 + x1)//2, (y0 + y1)//2
        canvas.create_text(midX, midY, text = text, font = 'Courier 26 bold', fill = 'gray')

    # draws the intro box
    def drawIntro(self, canvas):
        x0, y0, x1, y1 = self.width//2 - 2*self.incrementX, self.height//2 - self.incrementY, self.width//2 + 2*self.incrementX, self.height//2 + self.incrementY

        self.app.calendar.drawRoundedRectangle(canvas, x0, y0, x1, y1, 20, 'alice blue', 'gray', 5)

        text = "Hi! What's your name?"
        midX, midY = (x0 + x1)//2, (y0 + y1)//2
        canvas.create_text(midX, midY - self.incrementY//4, text = text, font = 'Courier 40 bold', fill = 'gray')

        self.drawInputName(canvas, midX, midY)
        self.drawYesNo(canvas, midX, midY)
    
    # draws the welcome box (for recurring/new players)
    def drawWelcome(self, canvas):
        x0, y0, x1, y1 = self.width//2 - 2*self.incrementX, self.height//2 - self.incrementY, self.width//2 + 2*self.incrementX, self.height//2 + self.incrementY
        
        self.app.calendar.drawRoundedRectangle(canvas, x0, y0, x1, y1, 20, 'alice blue', 'gray', 5)
        
        midX, midY = (x0 + x1)//2, (y0 + y1)//2
        
        if self.recurringPlayer: 
            text = 'Welcome back!\nWould you like to\ncontinue where you left off?'
            self.drawContinueNewGame(canvas, midX, midY)
        elif self.newPlayer:
            text = "well now it's Alice\nGood luck!"
            self.drawOk(canvas, midX, midY)
        
        
        canvas.create_text(midX, midY - self.incrementY//4, text = text, font = 'Courier 36 bold', fill = 'gray')

    # draws the continue/new game buttons
    def drawContinueNewGame(self, canvas, x, y):
        continueColor = newGameColor = 'gray'
        
        if self.mouseOverContinue: continueColor = 'salmon'
        elif self.mouseOverNewGame: newGameColor = 'salmon'

        canvas.create_text(x - self.incrementX, y + self.incrementY//2, text = 'CONTINUE', font = 'Courier 26 bold', fill = continueColor)

        canvas.create_text(x + self.incrementX, y + self.incrementY//2, text = 'NEW GAME', font = 'Courier 26 bold', fill = newGameColor)

    # draws the ok button
    def drawOk(self, canvas, x, y):
        okColor = 'gray'
        if self.mouseOverOk: okColor = 'salmon'

        canvas.create_text(x, y + self.incrementY//2, text = 'OK', font = 'Courier 26 bold', fill = okColor)


    # from OmniBox file
    # draws input
    def drawInputName(self, canvas, x, y):
        if self.mouseOverInputArea == True:
            text = '___'
            color = 'salmon'
        else:
            text = '___'
            color = 'gray'


        if self.clickedOnInputArea == True:
            text = ''
        if len(self.inputtedValue) > 0:
            text = self.inputtedValue

        canvas.create_text(x, y + self.incrementY//6, text = text, fill = color, font = 'Courier 36 bold')

    # draws yes/no buttons
    def drawYesNo(self, canvas, x, y):
        yesColor = noColor = 'gray'
        
        if self.mouseOverYes: yesColor = 'salmon'
        elif self.mouseOverNo: noColor = 'salmon'

        canvas.create_text(x - self.incrementX, y + self.incrementY//2, text = 'YES', font = 'Courier 26 bold', fill = yesColor)

        canvas.create_text(x + self.incrementX, y + self.incrementY//2, text = 'NO', font = 'Courier 26 bold', fill = noColor)




