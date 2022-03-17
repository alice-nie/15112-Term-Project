
from cmu_112_graphics import *
import datingSimClasses as char
from Calendar import *
from Room import *
from DatingSim import *
# following cmu 112 graphic framework
# any quirky color names from http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter


class OmniBox(Mode):
    
    # initializes variables
    def appStarted(self):

        # need for importing
        self.width = 1440
        self.height = 778


        # omni box dimensions
        self.incrementX = self.width//15
        self.incrementY = self.height//10
        self.x0, self.y0 = self.width - (6*self.incrementX), self.height - (5*self.incrementY)
        self.x1, self.y1 = self.width, self.height - 1.75*self.incrementY
        self.midX, self.midY = (self.x0 + self.x1)//2, (self.y0 + self.y1)//2


        # input 
        self.mouseOverInputArea = False
        self.clickedOnInputArea = False
        self.inputtedValue = ''

        # buttons
        self.mouseOverYes = False
        self.mouseOverNo = False
        self.mouseOverOk = False

        # modes from moving around in room
        self.sleepMode = self.eatMode = self.studyOrClassMode = self.outsideMode = False 

        # study or class modes
        self.studyMode = self.classMode = False
        self.mouseOverStudy = False
        self.mouseOverClass = False

        # tabs
        self.mouseOverStats = False
        self.mouseOverShop = False
        self.statsMode = False
        self.shopMode = False

        # meals                        
        self.mealRejected = False
        self.adjustMealTime = False

        # study selection
        self.mouseOverBS = self.mouseOverMicroecon = self.mouseOver15112 = self.mouseOverCalc = self.mouseOverInterp = False
        self.studyBS = self.studyMicroecon = self.study15112 = self.studyCalc = self.studyInterp = False
        self.studyPage = False

        # shop
        self.mouseOverSellSleep = False
        self.mouseOverSellMeals = False
        self.mouseOverSellFun = False
        self.clickedOnSellSleep = False
        self.clickedOnSellMeals = False
        self.clickedOnSellFun = False


        

###############################################################################

    # distance formula
    def distance(self, x0, y0, x1, y1):
        return ((x0 - x1) ** 2 + (y0 - y1) ** 2) ** 0.5

    #  tracks mouse movement
    def mouseMoved(self, event):

        # for tabs
        xMargin, ySpace = 20, 20
        width = 2
        extension = 5
        x0, y0 = self.x0 + xMargin, self.y0 - ySpace
        x1, y1 = x0 + 5*xMargin, self.y0 - ySpace//2
        if x0 <= event.x <= x1 and y0 <= event.y <= y1 + extension:
            self.mouseOverStats = True
        else: self.mouseOverStats = False
        x0, y0 = x1, y0
        x1, y1 = x1 + 5*xMargin, y1
        if x0 <= event.x <= x1 and y0 <= event.y <= y1 + extension:
            self.mouseOverShop = True
        else: self.mouseOverShop = False


        radiusOfNotice = 30

        # for input             # CHANGE from self.studyMode
        if self.sleepMode or self.studyPage or self.outsideMode or self.clickedOnSellSleep or self.clickedOnSellFun:
            if self.distance(event.x, event.y, self.midX, self.midY) <= radiusOfNotice and not self.inputtedValue.startswith('You'):
                self.mouseOverInputArea = True
            else: self.mouseOverInputArea = False

        # for study vs dating sim 
        if self.studyOrClassMode:
            if self.distance(event.x, event.y, self.midX, self.midY - self.incrementY//4) <= radiusOfNotice:
                self.mouseOverStudy = True
            else: self.mouseOverStudy = False

            if self.distance(event.x, event.y, self.midX, self.midY + self.incrementY//1.5) <= radiusOfNotice:
                self.mouseOverClass = True
            else: self.mouseOverClass = False

        # for studying which class
        if self.studyMode:
            if self.distance(event.x, event.y, self.midX, self.midY - 2*self.incrementY//2) <= radiusOfNotice:
                self.mouseOverBS = True
            else: self.mouseOverBS = False
            if self.distance(event.x, event.y, self.midX, self.midY - self.incrementY//2) <= radiusOfNotice:
                self.mouseOverMicroecon = True
            else: self.mouseOverMicroecon = False
            if self.distance(event.x, event.y, self.midX, self.midY) <= radiusOfNotice:
                self.mouseOver15112 = True
            else: self.mouseOver15112 = False
            if self.distance(event.x, event.y, self.midX, self.midY + self.incrementY//2) <= radiusOfNotice:
                self.mouseOverCalc = True
            else: self.mouseOverCalc = False
            if self.distance(event.x, event.y, self.midX, self.midY + 2*self.incrementY//2) <= radiusOfNotice:
                self.mouseOverInterp = True
            else: self.mouseOverInterp = False


        # for buttons YES NO OK                                 # CHANGE from self.studyMode
        if self.sleepMode or self.outsideMode or self.eatMode or self.clickedOnSellSleep or self.clickedOnSellMeals or self.clickedOnSellFun:
            if self.distance(event.x, event.y, self.midX - self.incrementX, self.midY + self.incrementY) <= radiusOfNotice:
                self.mouseOverYes = True
            else: self.mouseOverYes = False

            if self.distance(event.x, event.y, self.midX + self.incrementX, self.midY + self.incrementY) <= radiusOfNotice:
                self.mouseOverNo = True
            else: self.mouseOverNo = False

                # changed from (self.sleepMode and self.inputtedValue.startswith('You') or...  also studymode to studypage
            if ( ((self.sleepMode or self.outsideMode or 
                self.clickedOnSellSleep or self.clickedOnSellMeals or self.clickedOnSellFun) and 
                ( self.inputtedValue.startswith('You') )) or self.mealRejected):
                if self.distance(event.x, event.y, self.midX, self.midY + self.incrementY) <= radiusOfNotice:
                    self.mouseOverOk = True
                else: self.mouseOverOk = False

        if self.studyPage and self.inputtedValue.endswith('0'):
            if self.distance(event.x, event.y, self.midX - self.incrementX, self.midY + self.incrementY) <= radiusOfNotice:
                self.mouseOverYes = True
            else: self.mouseOverYes = False
            if self.distance(event.x, event.y, self.midX + self.incrementX, self.midY + self.incrementY) <= radiusOfNotice:
                self.mouseOverNo = True
            else: self.mouseOverNo = False
        elif self.studyPage and self.inputtedValue.startswith('You'):
            if self.distance(event.x, event.y, self.midX, self.midY + self.incrementY) <= radiusOfNotice:
                self.mouseOverOk = True
            else: self.mouseOverOk = False
        if char.player.eatOrSell or char.player.checkQuota:
            if self.distance(event.x, event.y, self.midX, self.midY + self.incrementY) <= radiusOfNotice:
                self.mouseOverOk = True
            else: self.mouseOverOk = False



        # for SHOP
        if self.shopMode:
            if self.distance(event.x, event.y, self.midX, self.midY) <= radiusOfNotice:
                self.mouseOverSellSleep = True
            else: self.mouseOverSellSleep = False
            if self.distance(event.x, event.y, self.midX, self.midY + self.incrementY//2) <= radiusOfNotice:
                self.mouseOverSellMeals = True
            else: self.mouseOverSellMeals = False
            if self.distance(event.x, event.y, self.midX, self.midY + self.incrementY) <= radiusOfNotice:
                self.mouseOverSellFun = True
            else: self.mouseOverSellFun = False

    # performs actions according to where the mouse is pressed
    def mousePressed(self, event):

        # input 
        if self.mouseOverInputArea:                        
            #if (self.studyMode and not self.studyPage) or (self.shopMode):
            #    self.inputtedValue = '___'
            #    self.clickedOnInputArea = True
            #else:
            self.inputtedValue = ''
            self.clickedOnInputArea = True

        # classes
        if (self.mouseOverBS or self.mouseOverMicroecon or self.mouseOver15112 or self.mouseOverCalc or self.mouseOverInterp) and not self.studyPage:
            if self.mouseOverBS: self.studyBS = True
            elif self.mouseOverMicroecon: self.studyMicroecon = True
            elif self.mouseOver15112: self.study15112 = True
            elif self.mouseOverCalc: self.studyCalc = True
            elif self.mouseOverInterp: self.studyInterp = True
            self.studyPage = True # studymode, studysubject, and studypage simultaneously true
                            
         

        # shop
        if self.shopMode:
            if self.mouseOverSellSleep: 
                self.clickedOnSellSleep = True
                self.shopMode = False
            elif self.mouseOverSellMeals: 
                self.clickedOnSellMeals = True
                self.shopMode = False
            elif self.mouseOverSellFun: 
                self.clickedOnSellFun = True
                self.shopMode = False


        # buttons : YES, NO, OK
        if self.mouseOverYes:

            if self.sleepMode:
                ogSleep, ogHealth, ogStress = char.player.sleep, char.player.health, char.player.stress
                char.player.addSleep(int(self.inputtedValue))
                if char.player.eatOrSell:
                    #char.player.sleep -= int(self.inputtedValue)
                    char.player.sleep, char.player.health, char.player.stress = ogSleep, ogHealth, ogStress
                    self.clickedOnInputArea = False
                    char.player.timeBlocks[char.player.currentWeek][str(char.player.currentHour)].remove(('sleep', int(self.inputtedValue)))
                    return
                if char.player.showWarning: self.inputtedValue = char.player.warning
                else: self.inputtedValue = f'You slept {self.inputtedValue} hour(s)!'
                self.clickedOnInputArea = False

            elif self.eatMode:
                char.player.eatMeal()
                if char.player.currentHour - 1 == 12 or char.player.currentHour - 1 == 16: 
                    self.adjustMealTime = True
                else: self.adjustMealTime = False
                if 9 <= char.player.currentHour < 13: mealTime = 0
                elif 13 <= char.player.currentHour < 17: mealTime = 1
                else: mealTime = 2
                if char.player.showWarning == False:
                    if self.adjustMealTime: mealTime -= 1 # if current time is 13 (1), then it was 12 (0) when it happened
                    char.player.timeToEat[mealTime] = False

            elif self.outsideMode:
                ogFun, ogHealth, ogStress = char.player.fun, char.player.health, char.player.stress
                char.player.goOutside(int(self.inputtedValue))
                if char.player.eatOrSell:
                    char.player.fun, char.player.health, char.player.stress = ogFun, ogHealth, ogStress
                    char.player.timeBlocks[char.player.currentWeek][str(char.player.currentHour)].remove(('fun', int(self.inputtedValue)))
                    self.clickedOnInputArea = False
                    return
                self.inputtedValue = f'You had fun for {self.inputtedValue} minutes!'
                self.clickedOnInputArea = False

            # classes
            if self.studyPage and self.inputtedValue.endswith('0'):
                if self.studyBS:
                    ogFreeHours, ogAffectionPoints, ogStress = char.player.freeHoursLeft, char.BS.affectionPoints, char.player.stress
                    char.BS.addStudyPoints(int(self.inputtedValue))
                    if char.player.eatOrSell or char.player.checkQuota:
                        char.player.freeHoursLeft, char.BS.affectionPoints, char.player.stress = ogFreeHours, ogAffectionPoints, ogStress
                        char.player.timeBlocks[char.player.currentWeek][str(char.player.currentHour)].remove(('study', int(self.inputtedValue)))
                        self.clickedOnInputArea = False
                        self.studyBS = False 
                        return
                    self.inputtedValue = f'You studied for {self.inputtedValue} minutes!'
                    self.clickedOnInputArea = False
                    self.studyBS = False                


                elif self.studyMicroecon:
                    ogFreeHours, ogAffectionPoints, ogStress = char.player.freeHoursLeft, char.Microecon.affectionPoints, char.player.stress
                    char.Microecon.addStudyPoints(int(self.inputtedValue))
                    if char.player.eatOrSell: 
                        char.player.freeHoursLeft, char.Microecon.affectionPoints, char.player.stress = ogFreeHours, ogAffectionPoints, ogStress
                        char.player.timeBlocks[char.player.currentWeek][str(char.player.currentHour)].remove(('study', int(self.inputtedValue)))
                        self.clickedOnInputArea = False
                        self.studyMicroecon = False
                        return
                    self.inputtedValue = f'You studied for {self.inputtedValue} minutes!'
                    self.clickedOnInputArea = False
                    self.studyMicroecon = False

                elif self.study15112:
                    ogFreeHours, ogAffectionPoints, ogStress = char.player.freeHoursLeft, char.Cs15112.affectionPoints, char.player.stress
                    char.Cs15112.addStudyPoints(int(self.inputtedValue))
                    if char.player.eatOrSell:
                        char.player.freeHoursLeft, char.Cs15112.affectionPoints, char.player.stress = ogFreeHours, ogAffectionPoints, ogStress
                        char.player.timeBlocks[char.player.currentWeek][str(char.player.currentHour)].remove(('study', int(self.inputtedValue)))
                        self.clickedOnInputArea = False
                        self.study15112 = False
                        return
                    self.inputtedValue = f'You studied for {self.inputtedValue} minutes!'
                    self.clickedOnInputArea = False
                    self.study15112 = False

                elif self.studyCalc:
                    ogFreeHours, ogAffectionPoints, ogStress = char.player.freeHoursLeft, char.Calc.affectionPoints, char.player.stress
                    char.Calc.addStudyPoints(int(self.inputtedValue))
                    if char.player.eatOrSell:
                        char.player.freeHoursLeft, char.Calc.affectionPoints, char.player.stress = ogFreeHours, ogAffectionPoints, ogStress
                        char.player.timeBlocks[char.player.currentWeek][str(char.player.currentHour)].remove(('study', int(self.inputtedValue)))
                        self.clickedOnInputArea = False
                        self.studyCalc = False
                        return
                    self.inputtedValue = f'You studied for {self.inputtedValue} minutes!'
                    self.clickedOnInputArea = False
                    self.studyCalc = False

                elif self.studyInterp:
                    ogFreeHours, ogAffectionPoints, ogStress = char.player.freeHoursLeft, char.Interp.affectionPoints, char.player.stress
                    char.Interp.addStudyPoints(int(self.inputtedValue))
                    if char.player.eatOrSell:
                        char.player.freeHoursLeft, char.Interp.affectionPoints, char.player.stress = ogFreeHours, ogAffectionPoints, ogStress
                        char.player.timeBlocks[char.player.currentWeek][str(char.player.currentHour)].remove(('study', int(self.inputtedValue)))
                        self.clickedOnInputArea = False
                        self.studyInterp = False
                        return
                    self.inputtedValue = f'You studied for {self.inputtedValue} minutes!'
                    self.clickedOnInputArea = False
                    self.studyInterp = False

            # shop
            elif self.clickedOnSellSleep:
                char.player.sellSleep(int(self.inputtedValue))
                if char.player.showWarning: self.inputtedValue = char.player.warning
                else: self.inputtedValue = f'You sold {self.inputtedValue} hour(s) of sleep!'
                self.clickedOnInputArea = False
                
            
            elif self.clickedOnSellMeals:
                char.player.sellMeal()
                if char.player.showWarning: self.inputtedValue = char.player.warning
                else: self.inputtedValue = f'You sold 1 hour of mealtime!'
                self.clickedOnInputArea = False
                

            elif self.clickedOnSellFun:
                char.player.sellFun(int(self.inputtedValue))
                if char.player.showWarning: self.inputtedValue = char.player.warning
                else: self.inputtedValue = f'You sold {self.inputtedValue} minute(s) of fun!'
                self.clickedOnInputArea = False

            self.mouseOverYes = False
                

        elif self.mouseOverNo:

            # re-enter           
            if self.sleepMode or self.outsideMode:
                self.inputtedValue = '___'
                self.clickedOnInputArea = False    

            if self.studyPage:
                self.studyBS = self.studyMicroecon = self.study15112 = self.studyCalc = self.studyInterp = False
                self.inputtedValue = '___'
                self.studyMode, self.studyPage = True, False
                self.clickedOnInputArea = False
                self.mouseOverNo = False

            # go back to menu
            elif self.clickedOnSellSleep or self.clickedOnSellMeals or self.clickedOnSellFun:
                self.shopMode = True
                self.clickedOnSellSleep = self.clickedOnSellMeals = self.clickedOnSellFun = False
                self.mouseOverNo = False


            # oh.
            elif self.eatMode:
                self.mealRejected = True  

            self.mouseOverNo = False


        if self.mouseOverOk:

            
            if self.studyPage and self.inputtedValue.startswith('You'):
                self.studyPage = False

            if self.sleepMode or self.outsideMode or self.studyMode or self.clickedOnSellSleep or self.clickedOnSellMeals or self.clickedOnSellFun:
                self.inputtedValue = ''
                if char.player.showWarning == True: char.player.showWarning = False

            elif self.eatMode:
                self.mealRejected = False
                char.player.showWarning = False
            
            if char.player.eatOrSell or char.BS.noTime or char.Microecon.noTime or char.Cs15112.noTime or char.Calc.noTime or char.Interp.noTime:
                char.player.eatOrSell = char.BS.noTime = char.Microecon.noTime = char.Cs15112.noTime = char.Calc.noTime = char.Interp.noTime = False

            # shop
            if self.clickedOnSellSleep or self.clickedOnSellMeals or self.clickedOnSellFun:
                self.shopMode = True
                self.clickedOnSellSleep = self.clickedOnSellMeals = self.clickedOnSellFun = False
                self.mouseOverOk = False 

            self.mouseOverOk = False
    
        # tabs
        if self.mouseOverStats:
            self.statsMode, self.shopMode = True, False
            self.sleepMode = self.eatMode = self.studyMode = self.outsideMode = self.studyOrClassMode = self.shopMode = self.studyBS = self.studyMicroecon = self.study15112 = self.studyCalc = self.studyInterp = False
            self.clickedOnSellSleep = self.clickedOnSellMeals = self.clickedOnSellFun = False

        elif self.mouseOverShop:
            self.shopMode, self.statsMode = True, False
            self.sleepMode = self.eatMode = self.studyMode = self.outsideMode = self.studyOrClassMode = self.statsMode = self.studyBS = self.studyMicroecon = self.study15112 = self.studyCalc = self.studyInterp = False


        if self.studyOrClassMode:
            if self.mouseOverStudy:
                self.studyMode = True
                self.studyOrClassMode = False
            elif self.mouseOverClass:
                self.classMode = True
                self.studyOrClassMode = False

    def keyPressed(self, event):
        if self.sleepMode or self.clickedOnSellSleep:
            if self.clickedOnInputArea:
                if event.key.isdigit:
                    self.inputtedValue += str(event.key)
                    self.clickedOnInputArea = False

        if self.outsideMode or self.studyMode or self.clickedOnSellFun:
            if self.clickedOnInputArea:
                if  event.key != '0' and event.key.isdigit:
                    self.inputtedValue += event.key
                elif event.key == '0':
                    self.inputtedValue += '0'
                    self.clickedOnInputArea = False
                            


###############################################################################


    # draws everything
    def redrawAll(self, canvas):
        #canvas.create_image(self.width//2, self.height//2, image = ImageTk.PhotoImage(self.roomPlain))
        self.drawOmniBox(canvas)
        if char.player.eatOrSell:
            self.drawEatOrSell(canvas)
        elif char.BS.noTime or char.Microecon.noTime or char.Cs15112.noTime or char.Calc.noTime or char.Interp.noTime:
            self.drawCheckQuota(canvas)
        elif self.sleepMode:
            self.drawSleepDialogue(canvas)
        elif self.eatMode:
            self.drawMealDialogue(canvas)
        elif self.outsideMode:
            self.drawDoorDialogue(canvas)
        elif self.studyOrClassMode:
            self.drawStudyDeskDialogue(canvas)
        elif self.studyMode:
            if self.studyPage == True:
                self.drawStudyDialogue(canvas)
            else:
                self.drawStudyWhichClass(canvas)

        elif (self.statsMode == False and self.shopMode == False and self.sleepMode == False and self.eatMode == False and self.outsideMode == False and self.studyOrClassMode == False and self.studyMode == False
            and self.clickedOnSellSleep == False and self.clickedOnSellMeals == False and self.clickedOnSellFun == False):
            self.drawIntroduction(canvas)
        elif self.statsMode:
            self.drawStatsDialogue(canvas)
        elif self.shopMode:
            self.drawShopDialogue(canvas)
        elif self.clickedOnSellSleep:
            self.drawSellSleep(canvas)
        elif self.clickedOnSellMeals:
            self.drawSellMeals(canvas)
        elif self.clickedOnSellFun:
            self.drawSellFun(canvas)

    def drawOmniBox(self, canvas):
        
        # outline
        oC,fC = 'gray', 'peachPuff2'
        cr = 20
        width = 7
        canvas.create_arc(self.x0, self.y0, self.x0 + 2*cr, self.y0 + 2*cr, start = 90, extent = 90, fill = fC, outline = oC, width = width)
        canvas.create_polygon(self.x0 + cr, self.y0, self.x1, self.y0, self.x1, self.y1, self.x0, self.y1, self.x0, self.y0 + cr, self.x0 + cr, self.y0 + cr, fill = fC, outline = oC, width = width)
        canvas.create_line(self.x0 + (width/2), self.y0 + cr, self.x0 + cr + width, self.y0 + cr, fill = fC, width = width * 1.5)
        canvas.create_line(self.x0 + cr, self.y0 + cr, self.x0 + cr, self.y0 + (width/2), fill = fC, width = width * 1.5)


        xMargin = 20
        ySpace = 20
        width = 2
        # draw tab 1:
        extension = 5
        x0, y0 = self.x0 + xMargin, self.y0 - ySpace
        x1, y1 = x0 + 5*xMargin, self.y0 - ySpace//2
        midX, midY = (x0+x1)//2, (y0+y1)//2

        if self.mouseOverStats or self.statsMode: color = 'peachPuff2'
        else: color = 'peachPuff3'

        
        canvas.create_arc(x0, y0, x0 + 2*cr, y0 + 2*cr + extension, start = 90, extent = 90, outline = color, width = width, fill = color)
        canvas.create_rectangle(x0 + cr, y0, x1 - cr, y0 + cr + (extension/2), fill = color, outline = color, width = width)
        canvas.create_arc(x1 - 2*cr, y0, x1, y0 + 2*cr + extension, start = 0, extent = 90, outline = color, width = width, fill = color)

        canvas.create_text(midX, midY + ySpace//2, text = 'STATS', font = 'Courier 16 bold', fill = 'gray')
        
        # draw tab 2:
        extension = 5
        x0, y0 = x1, y0
        x1, y1 = x1 + 5*xMargin, y1
        midX, midY = (x0+x1)//2, (y0+y1)//2

        if self.mouseOverShop or self.shopMode or self.clickedOnSellSleep or self.clickedOnSellMeals or self.clickedOnSellFun: color = 'peachPuff2'
        else: color = 'peachPuff3'

        canvas.create_arc(x0, y0, x0 + 2*cr, y0 + 2*cr + extension, start = 90, extent = 90, outline = color, width = width, fill = color)
        canvas.create_rectangle(x0 + cr, y0, x1 - cr, y0 + cr + (extension/2), fill = color, outline = color, width = width)
        canvas.create_arc(x1 - 2*cr, y0, x1, y0 + 2*cr + extension, start = 0, extent = 90, outline = color, width = width, fill = color)

        canvas.create_text(midX, midY + ySpace//2, text = 'SHOP', font = 'Courier 16 bold', fill = 'gray')
        
    def drawInputSlot(self, canvas):

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

        canvas.create_text(self.midX, self.midY - self.incrementY//4, text = text, fill = color, font = 'Courier 30 bold')

    def drawYesNo(self, canvas):

        yesColor = noColor = 'gray'
        
        if self.mouseOverYes: yesColor = 'salmon'
        elif self.mouseOverNo: noColor = 'salmon'

        canvas.create_text(self.midX - self.incrementX, self.midY + self.incrementY, text = 'YES', font = 'Courier 26 bold', fill = yesColor)

        canvas.create_text(self.midX + self.incrementX, self.midY + self.incrementY, text = 'NO', font = 'Courier 26 bold', fill = noColor)

    def drawOk(self, canvas):
        color = 'gray'
        if self.mouseOverOk: color = 'salmon'
        canvas.create_text(self.midX, self.midY + self.incrementY, text = 'OK', font = 'Courier 26 bold', fill = color)

    def drawSleepDialogue(self, canvas):
        if not self.inputtedValue.startswith('You'):
            canvas.create_text(self.midX - self.incrementX//10, self.midY - self.incrementY//4, text = 'Sleep for\thour(s)?', font = 'Courier 26 bold', fill = 'gray')
        self.drawInputSlot(canvas)
        if self.inputtedValue.startswith('You'):
            self.drawOk(canvas)
        elif len(self.inputtedValue) > 0 and self.inputtedValue != '___':
            self.drawYesNo(canvas)

    def drawMealDialogue(self, canvas):
        
        if 9 <= char.player.currentHour < 13: mealTime = 0
        elif 13 <= char.player.currentHour < 17: mealTime = 1
        else: mealTime = 2
        if self.adjustMealTime: check = mealTime - 1
        else: check = mealTime
    
        if self.mealRejected:
            canvas.create_text(self.midX, self.midY - self.incrementY//4, text = 'oh.', font = 'Courier 26 bold', fill = 'gray')
            self.drawOk(canvas)
        elif char.player.timeToEat[mealTime] and char.player.showWarning == False:            
            canvas.create_text(self.midX, self.midY - self.incrementY//4, text = 'Eat a meal?', font = 'Courier 26 bold', fill = 'gray')
            self.drawYesNo(canvas)
        elif char.player.showWarning:
            canvas.create_text(self.midX, self.midY - self.incrementY//4, text = char.player.warning, font = 'Courier 26 bold', fill = 'gray')
            self.drawOk(canvas)
        elif char.player.timeToEat[mealTime] == False:
            if check == 0: mealPeriod = '1 pm - 5 pm'
            elif check == 1: mealPeriod = '5 pm - 9 pm'
            else: mealPeriod = '9 am - 1 pm'
            canvas.create_text(self.midX, self.midY - self.incrementY//4, text = f'You ate a meal!\nNext meal period : {mealPeriod}', font = 'Courier 26 bold', fill = 'gray')

    def drawDoorDialogue(self, canvas):
        if not self.inputtedValue.startswith('You'):
            canvas.create_text(self.midX + self.incrementX//2.5, self.midY - self.incrementY//2, text = '  Go outside\n\nfor\t  minutes?', font = 'Courier 26 bold', fill = 'gray')
        self.drawInputSlot(canvas)
        if self.inputtedValue.startswith('You'):
            self.drawOk(canvas)
        elif self.inputtedValue.endswith('0') and self.inputtedValue != '___':
            self.drawYesNo(canvas)

    def drawStudyDeskDialogue(self, canvas):
        studyColor = classColor = 'gray'
        if self.mouseOverStudy: studyColor = 'salmon'
        elif self.mouseOverClass: classColor = 'salmon'
        canvas.create_text(self.midX, self.midY - self.incrementY//4, text = 'Study', font = 'Courier 26 bold', fill = studyColor)
        canvas.create_text(self.midX, self.midY + self.incrementY//1.5, text = 'Go to class', font = 'Courier 26 bold', fill = classColor)

    def drawStudyWhichClass(self, canvas):
        color1 = color2 = color3 = color4 = color5 = 'gray'
        if self.mouseOverBS: color1 = 'salmon'
        elif self.mouseOverMicroecon: color2 = 'salmon'
        elif self.mouseOver15112: color3 = 'salmon'
        elif self.mouseOverCalc: color4 = 'salmon'
        elif self.mouseOverInterp: color5 = 'salmon'
        canvas.create_text(self.midX, self.midY - 2*self.incrementY//2, text = 'Business Science', font = 'Courier 18 bold', fill = color1)
        canvas.create_text(self.midX, self.midY - self.incrementY//2, text = 'Microecon', font = 'Courier 18 bold', fill = color2)
        canvas.create_text(self.midX, self.midY, text = '15112', font = 'Courier 18 bold', fill = color3)
        canvas.create_text(self.midX, self.midY + self.incrementY//2, text = 'Calc in 3D', font = 'Courier 18 bold', fill = color4)
        canvas.create_text(self.midX, self.midY + 2*self.incrementY//2, text = 'Interp', font = 'Courier 18 bold', fill = color5)
            
    def drawStudyDialogue(self, canvas):
        if not self.inputtedValue.startswith('You'):
            canvas.create_text(self.midX - self.incrementX//10, self.midY - self.incrementY//4, text = 'Study for\tminutes?', font = 'Courier 26 bold', fill = 'gray')
        self.drawInputSlot(canvas)
        if self.inputtedValue.startswith('You'):
            self.drawOk(canvas)
        elif self.inputtedValue.endswith('0') and self.inputtedValue != '___':
            self.drawYesNo(canvas)

    def drawIntroduction(self, canvas):
        canvas.create_text(self.midX, self.midY, text = "Welcome to Alice's Suffering", font = 'Courier 26 bold', fill = 'gray')

    def drawStatsDialogue(self, canvas):
        if char.player.currentHour == 0:
            timeOfDay = 'am'
            hour = '12'
        elif char.player.currentHour > 12:
            timeOfDay = 'pm'
            hour = str(char.player.currentHour % 12)
            if hour == '0': hour = '12'
        else: 
            timeOfDay = 'am'
            hour = str(char.player.currentHour)
        
        if char.player.currentMinute == 0:
            minutes = str(char.player.currentMinute) + '0'
        else: minutes = str(char.player.currentMinute) # in 10s

        month = ['September', 'October', 'November', 'December'][char.player.currentMonth]
        day = char.player.currentDay
        
        canvas.create_text(self.midX, self.midY - self.incrementY - 20, text = f'Time: {hour}:{minutes} {timeOfDay}', font = 'Courier 18 bold', fill = 'gray')
        canvas.create_text(self.midX, self.midY - self.incrementY , text = f'Date: {month}/{day}/2020', font = 'Courier 18 bold', fill = 'gray')
        canvas.create_text(self.midX, self.midY - self.incrementY//2, text = f'Free hours left: {char.Alice.round(char.player.freeHoursLeft)} hour(s)', font = 'Courier 20 bold', fill = 'gray')
        canvas.create_text(self.midX, self.midY, text = f'Sleep quota remaining: {8 - char.player.sleep - char.player.soldSleep} hour(s)', font = 'Courier 20 bold', fill = 'gray')
        canvas.create_text(self.midX, self.midY + self.incrementY//2, text = f'Meal quota remaining: {3 - char.player.meals - char.player.soldMeals} meal(s)', font = 'Courier 20 bold', fill = 'gray')
        canvas.create_text(self.midX, self.midY + self.incrementY, text = f'Fun quota remaining: {3 - char.Alice.round(char.player.fun/60) - char.Alice.round(char.player.soldFun/60)} hour(s)', font = 'Courier 20 bold', fill = 'gray')

    def drawShopDialogue(self, canvas):
        sleepColor = mealColor = funColor = 'gray'
        if self.mouseOverSellSleep: sleepColor = 'steelblue1'
        elif self.mouseOverSellMeals: mealColor = 'khaki1'
        elif self.mouseOverSellFun: funColor = 'mediumblue'
        canvas.create_text(self.midX, self.midY - self.incrementY, text = "Welcome to school.\nSell your health for time.", font = 'Courier 24 bold', fill = 'gray')
        canvas.create_text(self.midX, self.midY, text = 'Sleep', font = 'Courier 24 bold', fill = sleepColor)
        canvas.create_text(self.midX, self.midY + self.incrementY//2, text = 'Meals', font = 'Courier 24 bold', fill = mealColor)
        canvas.create_text(self.midX, self.midY + self.incrementY, text = 'Fun', font = 'Courier 24 bold', fill = funColor)

    def drawSellSleep(self, canvas):
        if not self.inputtedValue.startswith('You'):
            canvas.create_text(self.midX  + self.incrementX//4, self.midY, text = 'Sell    \t hour(s)\n  of sleep?', font = 'Courier 26 bold', fill = 'gray')
        self.drawInputSlot(canvas)
        if self.inputtedValue.startswith('You'):
            self.drawOk(canvas)
        elif len(self.inputtedValue) > 0 and self.inputtedValue != '___':
            self.drawYesNo(canvas)

    def drawSellMeals(self, canvas):
        if not self.inputtedValue.startswith('You'):
            canvas.create_text(self.midX, self.midY - self.incrementY//4, text = 'Sell a meal?', font = 'Courier 26 bold', fill = 'gray')
            self.drawYesNo(canvas)
        else:
            canvas.create_text(self.midX, self.midY - self.incrementY//4, text = self.inputtedValue, font = 'Courier 26 bold', fill = 'gray')
            self.drawOk(canvas)

    def drawSellFun(self, canvas):
        if not self.inputtedValue.startswith('You'):
            canvas.create_text(self.midX  + self.incrementX//4, self.midY, text = '  Sell      minute(s)\n    of fun?', font = 'Courier 26 bold', fill = 'gray')        
        self.drawInputSlot(canvas)
        if self.inputtedValue.startswith('You'):
            self.drawOk(canvas)
        elif len(self.inputtedValue) > 0 and self.inputtedValue != '___':
            self.drawYesNo(canvas)

    def drawEatOrSell(self, canvas):
        if char.player.currentHour < 13: time = '1 pm'
        elif char.player.currentHour < 17: time = '5 pm'
        elif char.player.currentHour < 21: time = '9 pm'
        canvas.create_text(self.midX  + self.incrementX//4, self.midY, text = f'Action unavailable.\nA mealtime is ending!\nEither eat or sell a meal before {time}', font = 'Courier 20 bold', fill = 'gray')
        self.drawOk(canvas)

    def drawCheckQuota(self, canvas):
        canvas.create_text(self.midX + self.incrementX//4, self.midY, text = 'Action unavailable.\nCheck remaining quota requirements', font = 'Courier 24 bold', fill = 'gray')
        self.drawOk(canvas)