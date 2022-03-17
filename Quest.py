from cmu_112_graphics import *
import datingSimClasses as char
import random


class Quest(Mode):

    # initalize variables
    def appStarted(self):
        
        self.width, self.height = 1440, 778

        # for the quest box
        spacingX = self.width//5
        spacingY = self.height//6
        self.x0, self.y0 = self.width//2 - spacingX, self.height//2 - 1.5*spacingY
        self.x1, self.y1 = self.width//2 + spacingX, self.height//2 + 1.5*spacingY

        self.questText = 'T-T'

        # mock variables
        self.health = self.sleep = self.fun = 0
        self.sleepQuota = 8
        self.freeHoursLeft = 10
        self.BSlvl = self.Microlvl = self.CSlvl = self.Calclvl = self.Interplvl = 0
        self.productivity = 0
        self.stress = 0
        self.funQuota = 0
        
        self.revertHealth = self.revertProductivity = self.revertStress = 0

        # time variables
        self.week = char.player.currentWeek
        
        self.startAction = ''
    
    #######################################################################

    # for testing purposes (not using w/ Main)
    def mousePressed(self, event):
        self.bestCourseOfAction()

    # wrapper that initializes mock variables; calls solveAlicesSuffering for 7 different starting actions (studying (5), sleeping, going out)
    # finds action that maximizes health first and then change in total affection points
    def bestCourseOfAction(self):
        results = []

        for action in ['studyBS', 'studyMicro', 'studyCS', 'studyCalc', 'studyInterp', 'sleep', 'goOutside']:
            
            # initialize mock variables each time you test a starting action
            self.productivity = char.player.productivity
            self.stress = char.player.stress
            self.health = char.player.health
            self.sleep = char.player.sleep
            self.fun = char.player.fun
            self.sleepQuota = 8 - char.player.sleep - char.player.soldSleep
            self.funQuota = 3 - char.player.fun - char.player.soldFun
            self.freeHoursLeft = char.player.freeHoursLeft
            self.BSlvl = char.BS.affectionPoints
            self.Microlvl = char.Microecon.affectionPoints
            self.CSlvl = char.Cs15112.affectionPoints
            self.Calclvl = char.Calc.affectionPoints
            self.Interplvl = char.Interp.affectionPoints
            (self.revertBSlvl, self.revertMicrolvl, self.revertCSlvl, 
            self.revertCalclvl, self.revertInterplvl) = self.BSlvl, self.Microlvl, self.CSlvl, self.Calclvl, self.Interplvl

            
            results.append(self.solveAlicesSuffering(char.player.currentHour, action))

        bestPath = None
        bestHealth = 0
        bestChange = 0
        for path in results:
            if path != False:
                health = path[1]
                if health > bestHealth:
                    bestPath = path
                    bestHealth = health
                if health == bestHealth:
                    change = sum(path[2:7])/5
                    if change > bestChange:
                        bestPath = path
                        bestChange = change

        if bestPath == None: self.questText = '...'
        elif bestPath[0] == 'sleep': self.questText = 'Sleep'
        elif bestPath[0] == 'goOutside': self.questText = 'Have fun'
        elif bestPath[0] == 'studyBS': self.questText = 'Hang out with Willow'
        elif bestPath[0] == 'studyMicro': self.questText = 'Hang out with Karl'
        elif bestPath[0] == 'studyCS': self.questText = 'Hang out with Kimchee'
        elif bestPath[0] == 'studyCalc': self.questText = 'Hang out with Pain(e)'
        elif bestPath[0] == 'studyCalc': self.questText = 'HANG OUT WITH BEST BOI'
        
        
    # recursively goes through all 7 possible options (exluding eating and selling) to find route that'd keep health above current
    # player health or 70 (whatever is the min)
    # returns a list of the action, resulting health, and change in affection points
    def solveAlicesSuffering(self, hour, action, times = 0):
        if hour == 24:
            hour = 0
            self.week = (self.week + 1) % 7

        # end of day and healthier than current state/70 
        if hour == 9 and times != 0 and self.health >= min(char.player.health, 70):
            return True
        
        if self.classInSession(hour): 
            if self.week == 'SAT': # collab is 3 hours
                self.solveAlicesSuffering(hour + 3, action, times + 3)
            else: 
                self.solveAlicesSuffering(hour + 1, times + 1) # we'll say a class takes ~ hour 
        
        if hour == char.player.currentHour and times == 0: 
            self.startAction = action
            self.solveAlicesSuffering(hour + 1, action, times + 1) # startingAction
        
        for action in ['studyCalc', 'studyCS', 'studyMicro', 'studyBS', 'studyInterp', 'sleep', 'goOutside']:
            if self.isHealthy(hour, action):
                self.revertHealth = self.health
                self.revertProductivity = self.productivity
                self.revertStress = self.stress
                self.revertBSlvl, self.revertMicrolvl, self.revertCSlvl, self.revertCalclvl, self.revertInterplvl = self.BSlvl, self.Microlvl, self.CSlvl, self.Calclvl, self.Interplvl
                dBS = self.BSlvl - char.BS.affectionPoints
                dMicro = self.Microlvl - char.Microecon.affectionPoints
                d15112 = self.CSlvl - char.Cs15112.affectionPoints
                dCalc = self.Calclvl - char.Calc.affectionPoints
                dInterp = self.Interplvl - char.Interp.affectionPoints
                if self.solveAlicesSuffering(hour + 1, action, times + 1):
                    
                    return [self.startAction, self.health, dBS, dMicro, d15112, dCalc, dInterp]

            self.undo(hour, action)
        
        # if none of the actions work
        return False


    # uses mock variables to perform the action
    # returns True if health is above 70/current player health, and False otherwise
    def isHealthy(self, hour, action):
        if 'study' in action and self.freeHoursLeft <= 0: # no more free hours
            return False

        if action =='sleep' and self.sleepQuota == 0:
            return False

        if action == 'studyBS':
            # numbers taken from datingSimClasses 
            return self.study(2, action)
        elif action == 'studyMicro':
            return self.study(3, action)
        elif action == 'studyCS':
            return self.study(4, action)
        elif action == 'studyCalc':
            return self.study(5, action)
        elif action == 'studyInterp':
            return self.study(1, action)

        elif action == 'sleep':
            self.revertHealth = self.health
            self.revertProductivity = self.productivity
            self.revertStress = self.stress

            self.sleep += 1
            self.sleepQuota -= 1
            self.health += 5
            self.stress -= 3

            self.calculateStress()
            self.calculateProductivity()
            self.calculateHealth()
      
            return self.health > min(70, char.player.health)
        
        elif action == 'goOutside':
            self.revertHealth = self.health
            self.revertProductivity = self.productivity
            self.revertStress = self.stress
            
            if self.funQuota <= 3:
                self.fun += 1
                self.funQuota -= 1
            else:
                self.fun += 1 
                self.freeHoursLeft -= 1
            self.stress -= 3
            self.health += 2

            self.calculateStress()
            self.calculateProductivity()
            self.calculateHealth()

            return self.health > min(70, char.player.health)


    # undos the actions taken in isHealthy if it turns out False
    def undo(self, hour, action):
        if action == 'studyBS':
            self.undoStudy(2, action)
        elif action == 'studyMicro':
            self.undoStudy(3, action)
        elif action == 'studyCS':
            self.undoStudy(4, action)
        elif action == 'studyCalc':
            self.undoStudy(5, action)
        elif action == 'studyInterp':
            self.undoStudy(1, action)
        elif action == 'sleep':

            self.sleep -= 1
            self.sleepQuota += 1
            self.health -= 5
            self.stress += 3
            self.health = self.revertHealth
            self.productivity = self.revertProductivity
            self.stress = self.revertStress
            
        elif action == 'goOutside':
            if self.funQuota <= 3:
                self.fun -= 1
                self.funQuota += 1
            else:
                self.fun -= 1 
                self.freeHoursLeft += 1
            self.stress += 3
            self.health -= 2

            self.health = self.revertHealth
            self.productivity = self.revertProductivity
            self.stress = self.revertStress

    
    # helper for isHealthy that uses datingSimClasses info onto mock variables to perform action 'study'
    def study(self, difficulty, action):
        self.revertHealth = self.health
        self.revertProductivity = self.productivity
        self.revertStress = self.stress

        if action == 'studyBS': 
            self.BSlvl =  min( 500, self.BSlvl + char.Alice.round( (5 / (difficulty/2)) * (self.productivity/70)) )
        elif action == 'studyMicro': self.Microlvl =  min( 500, self.Microlvl + char.Alice.round( (5 / (difficulty/2)) * (self.productivity/70)) )
        elif action == 'studyCS': self.CSlvl =  min( 500, self.CSlvl + char.Alice.round( (5 / (difficulty/2)) * (self.productivity/70)) )
        elif action == 'studyCalc': self.Calclvl =  min( 500, self.Calclvl + char.Alice.round( (5 / (difficulty/2)) * (self.productivity/70)) )
        elif action == 'studyInterp': self.Interplvl =  min( 500, self.Interplvl + char.Alice.round( (5 / (difficulty/2)) * (self.productivity/70)) )
        
        self.stress += char.Alice.round(5 * (difficulty/6))
        self.freeHoursLeft -= 1
        self.health -= difficulty


        self.calculateStress()
        self.calculateProductivity()
        self.calculateHealth()


        return self.health >= min(70, char.player.health)



    # helper for undo that undos actions done with study
    def undoStudy(self, difficulty, action):
        if action == 'studyBS': self.BSlvl = self.revertBSlvl
        elif action == 'studyMicro': self.Microlvl = self.revertMicrolvl
        elif action == 'studyCS': self.CSlvl = self.revertCSlvl
        elif action == 'studyCalc': self.Calclvl  = self.revertCalclvl
        elif action == 'studyInterp': self.Interplvl  = self.revertInterplvl
        self.stress -= char.Alice.round(5 * (difficulty/6))
        self.freeHoursLeft += 1

        self.health = self.revertHealth
        self.productivity = self.revertProductivity
        self.stress = self.revertStress



    # following three calculations are simplified from datingSimClasses

    # calculates health based on current productivity
    def calculateHealth(self):
        if self.stress > 50:
            self.health = int(self.health - self.stress/25)
        
        if self.health >= 100:
            self.health = 100
        elif self.health <= 0:
            self.health = 0


    # calculates productivity based on current stress
    def calculateProductivity(self):
        productivity = self.productivity

        if self.stress > 50:
            productivity = int(self.productivity - self.stress/15) # can't do random so use average
        
        if self.health <= self.stress: self.productivity = min(50, productivity)
        else: self.productivity = productivity

        if self.productivity >= 100:
            self.productivity = 100
        elif self.productivity <= 0:
            self.productivity = 0
    

    # calculates stress based on current health and productivity
    def calculateStress(self):
        stress = self.stress
        if self.productivity <= 40: stress += 2
        
        if self.sleep <= 4: self.stress = max(40, stress)
        else: self.stress = stress

        if self.stress >= 100:
            self.stress = 100
        elif self.stress <= 0:
            self.stress = 0



    # returns True if there's a class that hour; false otherwise (assume player will go to class)
    def classInSession(self, hour):
        if self.week == 1: # 'MON'
            if hour == 12 or hour == 1 or hour == 5: # econ, calc, interp
                return True
        elif self.week == 2:
            if hour == 12 or hour == 3 or hour == 5: # BS, CS, Calc
                return True 
        elif self.week == 3: 
            if hour == 12 or hour == 1 or hour == 4 or hour == 5: # micro, calc, cs, interp
                return True
        elif self.week == 4:
            if hour == 12 or hour == 3: # BS, CS
                return True
        elif self.week == 5:
            if hour == 12 or hour == 1 or hour == 4 or hour == 5: # micro, calc, CS, interp
                return True
        elif self.week == 6:
            if hour == 9: # collab
                return True
        return False

        
    

    

    #######################################################################
       
    # draws everything
    def redrawAll(self, canvas):
        self.drawRoundedRectangle(canvas, self.x0, self.y0, self.x1, self.y1, 20, 'lightsteelblue1', 'gray', 5)

        text = self.questText
        midX, midY = (self.x0 + self.x1)//2, (self.y0 + self.y1)//2
        canvas.create_text(midX, midY, text = f'Quest:\n{self.questText}\nfor an hour', font = 'Courier 36 bold', fill = 'gray')


    # from calendar

    # draws a rectangle with rounded corners (outline)
    def drawRoundedRectangle(self, canvas, x0, y0, x1, y1, cr, fillColor, outlineColor, width, fill = True):
        
        fColor, oColor = fillColor, outlineColor

    
        self.fillRoundedRectangle(canvas, x0, y0, x1, y1, cr, fColor, 0, fill)
        
        style = ARC
        canvas.create_line(x0 + cr, y0, x1 - cr, y0, fill = oColor, width = width)
        canvas.create_arc(x1 - 2*cr, y0, x1, y0 + 2*cr, start = 0, extent = 90, style = style, outline = oColor, width = width)
        canvas.create_line(x1, y0 + cr, x1, y1 - cr, fill = oColor, width = width)
        canvas.create_arc(x1 - 2*cr, y1 - 2*cr, x1, y1, start = 270, extent = 90, style = style, outline = oColor, width = width)
        canvas.create_line(x1 - cr, y1, x0 + cr, y1, fill = oColor, width = width)
        canvas.create_arc(x0, y1 - 2*cr, x0 + 2*cr, y1, start = 180, extent = 90, style = style, outline = oColor, width = width)
        canvas.create_line(x0, y1 - cr, x0, y0 + cr, fill = oColor, width = width)
        canvas.create_arc(x0, y0, x0 + 2*cr, y0 + 2*cr, start = 90, extent = 90, style = style, outline = oColor, width = width)

   
    # fills in the rounded rectangle (color blocking)
    def fillRoundedRectangle(self, canvas, x0, y0, x1, y1, cr, color, width, fill):
        if fill == True:
            canvas.create_arc(x1 - 2*cr, y0, x1, y0 + 2*cr, start = 0, extent = 90, fill = color, outline = color, width = width)
            canvas.create_arc(x0, y0, x0 + 2*cr, y0 + 2*cr, start = 90, extent = 90, fill = color, outline = color, width = width)
            canvas.create_rectangle(x0 + cr, y0, x1 - cr, y0 + cr, fill = color, outline = color, width = width)
            canvas.create_arc(x1 - 2*cr, y1 - 2*cr, x1, y1, start = 270, extent = 90, fill = color, outline = color, width = width)
            canvas.create_arc(x0, y1 - 2*cr, x0 + 2*cr, y1, start = 180, extent = 90, fill = color, outline = color, width = width)
            canvas.create_rectangle(x0 + cr, y1 - cr, x1 - cr, y1, fill = color, outline = color, width = width)
            canvas.create_rectangle(x0, y0 + cr, x0 + cr, y1 - cr, fill = color, outline = color, width = width)
            canvas.create_rectangle(x1 - cr, y0 + cr, x1, y1 - cr, fill = color, outline = color, width = width)
            canvas.create_rectangle(x0 + cr, y0 + cr, x1 - cr, y1 - cr, fill = color, outline = color, width = width)


#Quest(width = 1440, height = 778)
