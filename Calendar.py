# about this file: Creates the calendar and handles the prediction 

from cmu_112_graphics import *
# following cmu 112 graphic framework
# any quirky color names from http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
import datingSimClasses as char

class Calendar(Mode):

    # code for the following two functions taken from https://www.cs.cmu.edu/~112/notes/notes-graphics.html

    # viewToModel; takes in a specific points and returns the row, col
    def getCell(self, x, y):        
        row = int((y - self.calMargin) / self.cellHeight)
        col = int((x - self.calMargin) / self.cellWidth)
        return (row, col)

    # modelToView; takes in a row, col and returns a specific pixel point
    def getCellBounds(self, row, col):
        x0 = self.calX0 + (col * self.cellWidth)
        y0 = self.calY0 + (row * self.cellHeight)
        x1 = x0 + self.cellWidth
        y1 = y0 + self.cellHeight
        return (x0, y0, x1, y1)
    
    # initializes variables
    def appStarted(self):
                
        self.width = 1440
        self.height = 778
        
        # type of view
        self.monthlyView = True
        self.weeklyView = False
        self.dailyView = False

        self.currentState = 0
        self.timerDelay = 25
        
        self.rows = [5, 1, 1] # [monthly, weekly, daily]
        self.cols = [7, 7, 1]
        self.calMargin = self.height//6
        self.calX0 = self.calMargin
        self.calY0 = self.calMargin
        self.calX1 = self.width - self.calMargin
        self.calY1 = self.height - self.calMargin  

        self.weeks = ['SUN', 'MON', 'TUE', 'WED', 'THUR', 'FRI', 'SAT']
        self.currentWeek = 0

        self.monthInfo()

        self.gridWidth = self.calX1 - self.calX0
        self.gridHeight = self.calY1 - self.calY0
        self.cellWidth = self.gridWidth // self.cols[self.currentState]
        self.cellHeight = self.gridHeight // self.rows[self.currentState]

        self.mouseLocation = (None, None)
        
        self.buttonLocations()
        self.mouseInButtonLeft = False
        self.mouseInButtonRight = False
        self.mouseInHeader = False

        self.curveRadius = 20

        # daily view
        self.currentDate = [0, 1] # month index, date (use date to find the weekday w/ dictionary)
        self.viewingDay = 1

        self.predeterminedEvents()

        self.predictionInfo()
       
    # initializes variables that are useful for making predictions
    def predictionInfo(self):
        self.statsDictionary = dict()
        self.BSPrediction = self.MicroPrediction = self.CSPrediction = self.CalcPrediction = self.InterpPrediction = 0 # True if not 0
        self.sleepPrediction = 0
        self.mealPrediction = 0
        self.funPrediction = 0
        
    # initializes information about back/next buttons
    def buttonLocations(self):
        cellWidth = self.gridWidth // self.cols[0]
        cellHeight = self.gridHeight // self.rows[0]
        self.buttonLeftX = ((self.calX0 + cellWidth/4) + (self.calX0 + 3*(cellWidth/4)))/2
        self.buttonY = ((self.calY0 - cellHeight) + (self.calY0 - cellWidth/4))/2
        self.buttonRightX = ((self.calX1 - 3*(cellWidth/4)) + (self.calX1 - cellWidth/4))/2
        self.buttonRadius = 20
   
    # initializes month boards 
    def monthInfo(self):
        self.months = ['September', 'October', 'November', 'December']
        self.currentMonth = 0
        self.viewingMonth = self.currentMonth

        # self.month has weeknames as keys and their correspondating dates as values
        self.september = self.daysInWeekColsDict(2, 30) # starts on a Tuesday
        self.septemberBoard = self.createDateBoard(self.september)

        self.october = self.daysInWeekColsDict(4, 31)
        self.octoberBoard = self.createDateBoard(self.october)

        self.november = self.daysInWeekColsDict(0, 30)
        self.novemberBoard = self.createDateBoard(self.november)

        self.december = self.daysInWeekColsDict(2, 31)
        self.decemberBoard = self.createDateBoard(self.december)

        self.listOfMonths = [self.september, self.october, self.november, self.december]
        self.listOfMonthBoards = [self.septemberBoard, self.octoberBoard, self.novemberBoard, self.decemberBoard]

    # initializes courses  
    def predeterminedEvents(self):
        
        # dictionary for individual days
        self.septemberEvents = dict()
        self.octoberEvents = dict()
        self.novemberEvents = dict()
        self.decemberEvents = dict() 
        self.listOfMonthEvents = [self.septemberEvents, self.octoberEvents, self.novemberEvents, self.decemberEvents]

        # dictionary for the classes            
        self.classes = dict()
                                        # beginning time, end time, time of day, relevant days of week
        self.classes['15112 Fundamentals of Programming Lecture'] = [1520, 1640, 'TUE', 'THUR']
        self.classes['15112 Fundamentals of Programming Recitation'] = [1600, 1650, 'WED', 'FRI']
        self.classes['15112 Fundamentals of Programming Collab'] = [900, 1200, 'SAT']
        self.classes['73102 Intro to Microecon Lecture'] = [1200, 1250, 'MON', 'WED']
        self.classes['73102 Intro to Microecon Recitation'] = [1200, 1250, 'FRI']
        self.classes['21259 Calc in 3D Lecture'] = [1320, 1410, 'MON', 'WED', 'FRI']
        self.classes['21259 Calc in 3D Recitation'] = [1720, 1810, 'TUE']
        self.classes['76101 Interpretation and Argument Lecture'] = [1720, 1810, 'MON', 'WED', 'FRI']
        self.classes['70106 Business Science Lecture'] = [1140, 1300, 'TUE', 'THUR']  

        # mapping courses
        for i in range(4):
            for weekCol in self.listOfMonths[i]: 
                for course in self.classes:
                    if weekCol in self.classes[course]:
                        monthEvent = self.listOfMonthEvents[i]
                        for date in self.listOfMonths[i][weekCol]:
                            if date not in monthEvent:
                                monthEvent[date] = set()
                                monthEvent[date] = {course}
                            else:
                                monthEvent[date].add(course)
           
    # creates a dictionary that maps the weekname to the dates that fall on that day
    def daysInWeekColsDict(self, startDayWeek, endDay):
        monthDict = dict()
        count = 0
        firstDay = 1
        while count < 7:
            monthDict[self.weeks[startDayWeek]] = [i for i in range(firstDay, endDay + 1, 7)]
            firstDay += 1
            startDayWeek += 1
            count += 1
            if startDayWeek >= len(self.weeks): startDayWeek %= len(self.weeks)
        return monthDict
    
    # creates a 2d list of a month's dates (-1 when no date)
    def createDateBoard(self, month):
        rows, cols = self.rows[self.currentState], self.cols[self.currentState]
        for week in self.weeks:
            if 1 in month[week]:
                startIndex = self.weeks.index(week)

            if 31 in month[week]:
                endIndex = self.weeks.index(week)
            elif 30 in month[week]:
                endIndex = self.weeks.index(week)

        board = [ ([0] * cols) for row in range(rows) ]

        for row in range(rows):
            for col in range(cols):
                if row == 0 and col < startIndex:
                    board[row][col] = -1
                elif row == 4 and col > endIndex:
                    board[row][col] = -1
                else:
                    dayOfWeek = self.weeks[col]
                    if board[0][col] == -1:
                        board[row][col] = month[dayOfWeek][row - 1]
                    else:
                        board[row][col] = month[dayOfWeek][row]
        
        return board
    
    # distance formula
    def distance(self, x0, y0, x1, y1):
        return ((x0 - x1) ** 2 + (y0 - y1) ** 2) ** 0.5


###############################################################################

    # keeps track of where the mouse currently is
    def mouseMoved(self, event):
        # pops out the calendar dates
        if (self.calX0 <= event.x <= self.calX1 and self.calY0 <= event.y <= self.calY1):
            mouseRow, mouseCol = self.getCell(event.x, event.y)
            self.mouseLocation = mouseRow, mouseCol

        # pops out the buttons
        if self.distance(event.x, event.y, self.buttonLeftX, self.buttonY) <= self.buttonRadius:
            self.mouseInButtonLeft = True
        else: 
            self.mouseInButtonLeft = False
        
        if self.distance(event.x, event.y, self.buttonRightX, self.buttonY) <= self.buttonRadius:
            self.mouseInButtonRight = True
        else:
            self.mouseInButtonRight = False

        cellWidth = self.gridWidth // self.cols[0]
        cellHeight = self.gridHeight // self.rows[0]
        if ((self.calX0 + cellWidth <= event.x <= self.calX1 - cellWidth) and
            (self.calY0 - cellHeight <= event.y <= self.calY0 - cellHeight//3)):
            self.mouseInHeader = True
        else:
            self.mouseInHeader = False

    # performs actions based on where mouse is pressed
    def mousePressed(self, event):
        # back/next button functionality
        if not ((self.calX0 <= event.x <= self.calX1) and
            (0 <= event.y <= self.calY1)):
            return

        if self.mouseInButtonLeft:
            
            if self.monthlyView and self.viewingMonth != 0:
                self.viewingMonth -= 1
            
            elif self.dailyView:
                if (self.viewingMonth, self.viewingDay) !=  (0, 1):
                    if self.viewingDay == 1:
                        if self.viewingMonth == 2:
                            self.viewingDay = 31
                            self.viewingMonth -= 1
                        else:
                            self.viewingDay = 30
                            self.viewingMonth -= 1
                    else:
                        self.viewingDay -= 1
        
        elif self.mouseInButtonRight:
            
            if self.monthlyView and self.viewingMonth != (len(self.months) - 1):
                self.viewingMonth += 1
            
            elif self.dailyView:
                if (self.viewingMonth, self.viewingDay) != (3, 31):
                    if (self.viewingMonth == 0 or self.viewingMonth == 2) and self.viewingDay == 30:
                        self.viewingDay = 1
                        self.viewingMonth += 1
                    elif self.viewingDay == 31:
                        self.viewingDay  = 1
                        self.viewingMonth += 1
                    else:
                        self.viewingDay += 1

        # switching between viewtypes

        # month to day
        if self.monthlyView:
            row, col = self.mouseLocation
            monthBoard = self.listOfMonthBoards[self.viewingMonth]
            date = monthBoard[row][col]
            if date == -1:
                return
            else:
                if not self.mouseInButtonLeft and not self.mouseInButtonRight:
                    self.viewingDay = date
                    self.dailyView, self.monthlyView, self.currentState = True, False, 2
                    self.cellWidth = self.gridWidth // self.cols[self.currentState]
                    self.cellHeight = self.gridHeight // self.rows[self.currentState]
                    #if (char.player.currentMonth, char.player.currentDay) != (0, 30) and (char.player.currentMonth, char.player.currentDay) != (1, 1) and (char.player.currentMonth, char.player.currentDay) != (1, 2): ## less
                    self.makePrediction()

        # day to month
        if self.dailyView:
            if self.mouseInHeader:
                self.monthlyView, self.dailyView, self.currentState = True, False, 0
                self.cellWidth = self.gridWidth // self.cols[self.currentState]
                self.cellHeight = self.gridHeight // self.rows[self.currentState]

    # predictions are for studying, sleeping, going outside, or eating
    def makePrediction(self):
        
        # reset from previous
        self.BSPrediction = self.MicroPrediction = self.CSPrediction = self.CalcPrediction = self.InterpPrediction = 0 # True if not 0
        self.sleepPrediction = self.mealPrediction = self.funPrediction = self.studyPrediction = 0
        
        # look at previous days in that weekCol, identify trends, get stats for studying time
        for week in self.weeks: 
            if char.player.currentDay in self.listOfMonths[char.player.currentMonth][week]:
                weekDay = week 

        # use a scatter plot and find the slope of the best fitting line to identify  trends
        # obtain the 'coordinates' of that weekCol's stats
        
        #initialize
        selfStatsCollection, studyStatsCollection = self.statCollector()
        productivityTrend, sleepTrend, mealsTrend, funTrend = list(), list(), list(), list()
        BStrend, Microtrend, CStrend, Calctrend, Interptrend = list(), list(), list(), list(), list()
        productivitySlope = sleepSlope = mealsSlope = funSlope = 0
        productivitySD = sleepSD = mealsSD = funSD = 0
        BSSlope = MicroSlope = CSSlope = CalcSlope = InterpSlope = 0
        BSSD = MicroSD = CSSD = CalcSD = InterpSD = 0
        listOfCoursePredictions = [self.BSPrediction, self.MicroPrediction, self.CSPrediction, self.CalcPrediction, self.InterpPrediction]

        for i in range(0, char.player.currentMonth + 1): 
            for date in self.listOfMonths[i][weekDay]: 
                if date in selfStatsCollection[i]: 
                    for num in range(4):
                        [productivityTrend, sleepTrend, mealsTrend, funTrend][num].append((date, selfStatsCollection[i][date][num]))
                    for num in range(5):
                        [BStrend, Microtrend, CStrend, Calctrend, Interptrend][num].append((date, studyStatsCollection[i][date][num]))
        for i in range(4):
            [productivitySlope, sleepSlope, mealsSlope, funSlope][i] = self.lineOfBestFitSlope([productivityTrend, sleepTrend, mealsTrend, funTrend][i])
            [productivitySD, sleepSD, mealsSD, funSD][i] = self.findStandardDeviation([productivityTrend, sleepTrend, mealsTrend, funTrend][i])
        for i in range(5):
            [BSSlope, MicroSlope, CSSlope, CalcSlope, InterpSlope][i] = self.lineOfBestFitSlope([BStrend, Microtrend, CStrend, Calctrend, Interptrend][i])
            [BSSD, MicroSD, CSSD, CalcSD, InterpSD][i] = self.findStandardDeviation([BStrend, Microtrend, CStrend, Calctrend, Interptrend][i])
        
        # if within one standard deviation after five days (weekdays), go with the average (trend is significant if > 1 standard deviation)
        mostLikelyStudyingSlope = max(BSSlope, MicroSlope, CSSlope, CalcSlope, InterpSlope)
        index = [BSSlope, MicroSlope, CSSlope, CalcSlope, InterpSlope].index(mostLikelyStudyingSlope)
        trendList = [BStrend, Microtrend, CStrend, Calctrend, Interptrend]
        mostLikelyStudying = trendList[index]
        likelySD =  [BSSD, MicroSD, CSSD, CalcSD, InterpSD][index]

        # line for most likely studying subject
        xSum, ySum = 0, 0
        for i in range(len(mostLikelyStudying)):
            x, y = mostLikelyStudying[i]
            xSum += x
            ySum += y
        xMean = xSum / len(mostLikelyStudying)
        yMean = ySum / len(mostLikelyStudying)

        yIntercept = yMean - xMean * mostLikelyStudyingSlope
        projectionAfterFiveDays = 5*mostLikelyStudyingSlope + yIntercept
        if abs(projectionAfterFiveDays - yMean) < likelySD:
            timeSpent = yMean
        else:
            timeSpent = 1*mostLikelyStudyingSlope + yIntercept # trendlines use previous days' data
        

        # check just the past five day's trend; if there's a constant increase it may indicate project/test (if those were coded in)
        allTrendsForIndexing = []
        bestTrendLists = []
        for course in range(5):
            currentTrendList = []
            for day in range(char.player.currentDay - 1, char.player.currentDay - 6, -1):
                month = char.player.currentMonth
                if day < 1: 
                    if char.player.currentMonth == 2 or char.player.currentMonth == 4: day, month = 30 - abs(day), char.player.currentMonth - 1
                    elif char.player.currentMonth == 3: day, month = 31 - abs(day), char.player.currentMonth - 1
                currentTrendList.append(studyStatsCollection[month][day][course])
            # test if positive trend
            allTrendsForIndexing.append(currentTrendList)
            currentTrendList = list(reversed(currentTrendList))
            if currentTrendList[len(currentTrendList) - 1] - currentTrendList[0] > 0:
                for i in range(len(currentTrendList) - 1):
                    if currentTrendList[i] < currentTrendList[i+1]:
                        bestTrendLists.append(currentTrendList)
        distance = 0
        bestTrend = None
        for trend in bestTrendLists:
            tempDistance = trend[len(trend) - 1] - trend[0]
            if tempDistance > distance:
                bestTrend = trend
                distance = tempDistance
        
        if bestTrend != None:
            avgDistance = 0
            for day in range(len(bestTrend)-1):
                distance = bestTrend[day + 1] - bestTrend[day] 
                avgDistance += distance
            avgDistance //= (len(bestTrend) - 1)
            
            # new index and timeSpent
            index = allTrendsForIndexing.index(bestTrend)
            timeSpent = bestTrend[len(bestTrend)] + avgDistance
        
            listOfCoursePredictions = [self.sleepPrediction, self.mealPrediction, self.funPrediction, self.studyPrediction]
            listOfCoursePredictions[index] = timeSpent
            [self.sleepPrediction, self.mealPrediction, self.funPrediction, self.studyPrediction] = listOfCoursePredictions
            return

        # use weighted probabilities w/ time to see if its more likely they'd study, sleep, eat, or go have fun at the current time

        # weight is how often they do this action ~ this time (this hour and next)
        week = self.weeks.index(weekDay)
        listOfActions = char.player.timeBlocks[week][str(char.player.currentHour)] + char.player.timeBlocks[week][str((char.player.currentHour + 1) % 24)] + char.player.timeBlocks[week][str((char.player.currentHour - 1) % 24)]
        
        sleepCounter = mealCounter = funCounter = studyCounter = 0
        if len(listOfActions) == 0: # not enough info, so go with the study trend
            listOfCoursePredictions[index] = timeSpent
            [self.BSPrediction, self.MicroPrediction, self.CSPrediction, self.CalcPrediction, self.InterpPrediction] = listOfCoursePredictions
            return
        
        for action in listOfActions:
            act, time = action
            if act == 'sleep': sleepCounter += 1
            elif act == 'meal': mealCounter += 1
            elif act == 'fun': funCounter += 1
            elif act == 'study': studyCounter += 1

        total = sleepCounter + mealCounter + funCounter + studyCounter # weight
        sleepProb = sleepCounter / total
        mealProb = mealCounter / total
        funProb = funCounter / total
        studyProb = studyCounter / total

        mostProbable = max(sleepProb, mealProb, funProb, studyProb)
        selfIndex = [sleepProb, mealProb, funProb, studyProb].index(mostProbable) # find avg time
        timeAvg = 0
        for action in listOfActions:
            act, time = action
            if act == ['sleep', 'meal', 'fun', 'study'][selfIndex]:
                timeAvg += 1
        timeAvg /= [sleepCounter, mealCounter, funCounter, studyCounter][selfIndex]

        significantDifference = 5
        if mostProbable - studyProb < significantDifference and mostLikelyStudyingSlope > 0:
            listOfCoursePredictions[selfIndex] = timeSpent
            [self.BSPrediction, self.MicroPrediction, self.CSPrediction, self.CalcPrediction, self.InterpPrediction] = listOfCoursePredictions
            return
        
        else:
            listOfSelfPredictions = [self.sleepPrediction, self.mealPrediction, self.funPrediction, self.studyPrediction]
            listOfSelfPredictions[selfIndex] = timeAvg
            [self.sleepPrediction, self.mealPrediction, self.funPrediction, self.studyPrediction] = listOfSelfPredictions
            if self.studyPrediction != 0:
                listOfCoursePredictions[index] = timeSpent
                [self.BSPrediction, self.MicroPrediction, self.CSPrediction, self.CalcPrediction, self.InterpPrediction] = listOfCoursePredictions
            return

    # finds standard deviation of a trendlist
    def findStandardDeviation(self, trendList):
        mean = 0
        for i in range(len(trendList)):
            x, y = trendList[i]
            mean += y
        mean /= len(trendList)

        variance = 0
        for i in range(len(trendList)):
            x, y = trendList[i]
            variance += (y - mean) ** 2
        variance /= len(trendList)

        return variance ** 0.5

    # read up on least square method again and obtained formula at https://www.varsitytutors.com/hotmath/hotmath_help/topics/line-of-best-fit#:~:text=A%20line%20of%20best%20fit%20can%20be%20roughly%20determined%20using,as%20many%20points%20as%20possible).
    # finds the slope for the line of best fit for a trendlist
    def lineOfBestFitSlope(self, trendList):
        xSum, ySum = 0, 0
        for i in range(len(trendList)):
            x, y = trendList[i]
            xSum += x
            ySum += y
        xMean = xSum / len(trendList)
        yMean = ySum / len(trendList)

        numerator = 0
        denominator = 0
        for i in range(len(trendList)):
            x, y = trendList[i]
            xDist = x - xMean
            yDist = y - yMean
            numerator += (xDist) * (yDist)
            denominator += (xDist) ** 2
        
        slope = numerator/denominator
        return slope


    # list of dictionary's that track each day's stats (datingSimClasses houses the previous day's stats)
    # returns the list
    def statCollector(self):
        selfStatsCollection = []
        studyStatsCollection = []
        for i in range(0, char.player.currentMonth + 1):
            selfStatsCollection.append(dict()) 
            studyStatsCollection.append(dict())
            for row in range(self.rows[0]):
                for col in range(self.cols[0]):
                    date = self.listOfMonthBoards[i][row][col]
                    if (i < char.player.currentMonth and date != -1) or (i == char.player.currentMonth and -1 < date < char.player.currentDay):
                        day = row + col
                        selfStatsCollection[i][date] = [char.player.daysProductivity[i][day], char.player.daysSleep[i][day], char.player.daysMeals[i][day], char.player.daysFun[i][day]]
                        studyStatsCollection[i][date] = [char.BS.timeSpentStudying[i][day], char.Microecon.timeSpentStudying[i][day],
                                                         char.Cs15112.timeSpentStudying[i][day],  char.Calc.timeSpentStudying[i][day], char.Interp.timeSpentStudying[i][day]]
            
        return selfStatsCollection, studyStatsCollection


###############################################################################


    # draws everything
    def redrawAll(self, canvas):
        self.drawRoundedRectangle(canvas, self.calX0, self.calY0, self.calX1, self.calY1, self.curveRadius, 'lavender blush', 'gray', 7)
        
        self.drawHeader(canvas)
        self.drawButtons(canvas)

        if self.monthlyView:
            self.drawMonthlyView(canvas)
        elif self.dailyView:
            self.drawDailyView(canvas)
            
    # draws the rectangle for prediction
    def drawPrediction(self, canvas):


        if self.BSPrediction != 0: time, text = self.BSPrediction, 'Study Business Science'
        elif self.MicroPrediction != 0: time, text = self.MicroPrediction, 'Study Microecon'
        elif self.CSPrediction != 0: time, text = self.CSPrediction, 'Study 15112'
        elif self.CalcPrediction != 0: time, text = self.CalcPrediction, 'Study Calc'
        elif self.InterpPrediction != 0: time, text = self.InterpPrediction, 'Study Interp'
        elif self.sleepPrediction != 0: time, text = self.sleepPrediction, 'Sleep'
        elif self.mealPrediction != 0: time, text = self.mealPrediction, 'Eat'
        elif self.funPrediction != 0: time, text = self.funPrediction, 'Go outside'


        # time is in minutes
        beginningHour = char.player.currentHour
        beginningMinute = char.player.currentMinute
        if 'Study' in text or 'outside' in text: 
            hours = time // 60
            minutes = time - (60)*hours
            endHour = beginningHour + hours
            endMinute = beginningMinute + minutes
        else:
            endHour = (beginningHour + time) % 25
            endMinute = beginningMinute
        
        margin = 75
        dy = (self.calY1 - self.calY0)//12
        ddy = dy//6 # increments of 10 minutes
        
        endY = self.calY1
        endY -= 5 # account for outline width

        # format the text for time
        text = self.createEventText(beginningHour, beginningMinute, endHour, endMinute, text)
        color = 'khaki1'
        
        # from draw pretermined events
        if beginningHour < 12 and endHour > 12:
                endHour %= 12
                x0, x1 = self.calX0 + margin, self.width//2 - margin
                x2, x3 = self.width//2 + margin, self.calX1 - margin
                y0, y1 = self.calY0 + (beginningHour * dy) + ((beginningMinute//10) * ddy), endY
                y2, y3 = self.calY0, self.calY0 + (endHour * dy) + ((endMinute//10) * ddy) 

                self.drawEvents(canvas, x0, y0, x1, y1, 'gray', color, 3, text)
                self.drawEvents(canvas, x2, y2, x3, y3, 'gray', color, 3, text)

        elif beginningHour < 12 and endHour <= 12:
            x0, x1 = self.calX0 + margin, self.width//2 - margin
            y0 = self.calY0 + (beginningHour * dy) + ((beginningMinute//10) * ddy) 
            y1 = self.calY0 + (endHour * dy) + ((endMinute//10) * ddy) 
            self.drawEvents(canvas, x0, y0, x1, y1, 'gray', color, 3, text)

        elif beginningHour >= 12 and endHour >= 12:
            beginningHour %= 12
            endHour %= 12
            x0, x1 = self.width//2 + margin, self.calX1 - margin 
            y0 = self.calY0 + (beginningHour * dy) + ((beginningMinute//10) * ddy)
            y1 = self.calY0 + (endHour * dy) + ((endMinute//10) * ddy) 
            self.drawEvents(canvas, x0, y0, x1, y1, 'gray', color, 3, text)

    # draws a rectangle with rounded corners (outline)
    def drawRoundedRectangle(self, canvas, x0, y0, x1, y1, cr, fillColor, outlineColor, width, fill = True):
        
        fColor, oColor = fillColor, outlineColor

        if (y1 - y0) < self.curveRadius:
            self.drawThinRoundedRectangle(canvas, x0, y0, x1, y1, cr, fColor, oColor, width)
        else:
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

    # draws a thin "rectangle" with rounded corners (outline)
    def drawThinRoundedRectangle(self, canvas, x0, y0, x1, y1, cr, fillColor, outlineColor, width, fill = True):
        
        fColor, oColor = fillColor, outlineColor
        self.fillThinRoundedRectangle(canvas, x0, y0, x1, y1, cr, fColor, 0, fill)

        style = ARC
        canvas.create_arc(x0, y0, x0 + 2*cr, y1, start = 90, extent = 180, style = style, outline = oColor, width = width)
        canvas.create_line(x0 + cr, y0, x1 - cr, y0, fill = oColor, width = width)
        canvas.create_line(x0 + cr, y1, x1 - cr, y1, fill = oColor, width = width)
        canvas.create_arc(x1 - 2*cr, y0, x1, y1, start = 270, extent = 180, style = style, outline = oColor, width = width)

    # fills in the thin rectangle (color blocking)
    def fillThinRoundedRectangle(self, canvas, x0, y0, x1, y1, cr, color, width, fill):
        if fill == True:
            style = CHORD
            canvas.create_arc(x0, y0, x0 + 2*cr, y1, start = 90, extent = 180, style = style, fill = color, outline = color, width = width)
            canvas.create_rectangle(x0 + cr, y0, x1 - cr, y1, fill = color, width = width)
            canvas.create_arc(x1 - 2*cr, y0, x1, y1, start = 270, extent = 180, style = style, fill = color, outline = color, width = width)

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

    # draws the corner calendar dates so that one corner of the rectangle is rounded
    def drawRectangleWithCurvedCorner(self, canvas, x0, y0, x1, y1, cornerDir, outlineColor, fillColor, width):
        oC = outlineColor
        fC = fillColor
        cr = self.curveRadius
        if cornerDir == 'topLeft':
            canvas.create_arc(x0, y0, x0 + 2*cr, y0 + 2*cr, start = 90, extent = 90, fill = fC, outline = oC, width = width)
            canvas.create_polygon(x0 + cr, y0, x1, y0, x1, y1, x0, y1, x0, y0 + cr, x0 + cr, y0 + cr, fill = fC, outline = oC, width = width)
            canvas.create_line(x0 + (width/2), y0 + cr, x0 + cr + width, y0 + cr, fill = fC, width = width * 1.5)
            canvas.create_line(x0 + cr, y0 + cr, x0 + cr, y0 + (width/2), fill = fC, width = width * 1.5)
            
        elif cornerDir == 'topRight':
            canvas.create_arc(x1 - 2*cr, y0, x1, y0 + 2*cr, start = 0, extent = 90, fill = fC, outline = oC, width = width)
            canvas.create_polygon(x0, y0, x1 - cr, y0, x1 - cr, y0 + cr, x1, y0 + cr, x1, y1, x0, y1, fill = fC, outline = oC, width = width)
            canvas.create_line(x1 - cr, y0 + (width/2), x1 - cr, y0 + cr, fill = fC, width = width * 1.5)
            canvas.create_line(x1 - cr - width, y0 + cr, x1 - (width/2), y0 + cr, fill = fC, width = width * 1.5)
            
        elif cornerDir == 'bottomLeft':
            canvas.create_arc(x0, y1 - 2*cr, x0 + 2*cr, y1, start = 180, extent = 90, fill = fC, outline = oC, width = width)
            canvas.create_polygon(x0, y0, x1, y0, x1, y1, x0 + cr, y1, x0 + cr, y1 - cr, x0 , y1 - cr, fill = fC, outline = oC, width = width)
            canvas.create_line(x0 + (width/2), y1 - cr, x0 + cr + width, y1 - cr, fill = fC, width = width * 1.5)
            canvas.create_line(x0 + cr, y1 - cr, x0 + cr, y1 - (width/2), fill = fC, width = width * 1.5)
            
        elif cornerDir == 'bottomRight':
            canvas.create_arc(x1 - 2*cr, y1 - 2*cr, x1, y1, start = 270, extent = 90, fill = fC, outline = oC, width = width)
            canvas.create_polygon(x0, y0, x1, y0, x1, y1 - cr, x1 - cr, y1 - cr, x1 - cr, y1, x0, y1, fill = fC, outline = oC, width = width)
            canvas.create_line(x1 - cr - width, y1 - cr, x1 - (width/2), y1 -cr, fill = fC, width = width * 1.5)
            canvas.create_line(x1 - cr, y1 - cr, x1 - cr, y1 - (width/2), fill = fC, width = width * 1.5)
            
    # draws a rectangle with two rounded corners
    def drawTabs(self, canvas, x0, y0, x1, y1, cr, color, width):
        extension = 5
        canvas.create_arc(x0, y0, x0 + 2*cr, y0 + 2*cr + extension, start = 90, extent = 90, outline = color, width = width, fill = color)
        canvas.create_rectangle(x0 + cr, y0, x1 - cr, y0 + cr + (extension/2), fill = color, outline = color, width = width)
        canvas.create_arc(x1 - 2*cr, y0, x1, y0 + 2*cr + extension, start = 0, extent = 90, outline = color, width = width, fill = color)

    # draws the monthly view
    def drawMonthlyView(self, canvas):
        self.drawWeeks(canvas)

        rows, cols = self.rows[0], self.cols[0]
        for row in range(rows):
            for col in range(cols):
                x0, y0, x1, y1 = self.getCellBounds(row, col)

                if self.mouseLocation == (row, col):
                    width = 8
                    oColor = 'gray' # only half of a different color shows up
                    fColor = 'mistyrose'
                else: 
                    width = 5
                    oColor = 'gray'
                    fColor = 'lavender blush'

                if (row, col) == (0,0): 
                    self.drawRectangleWithCurvedCorner(canvas, x0, y0, x1, y1, 'topLeft', oColor, fColor, width)
                elif (row, col) == (0, cols - 1): 
                    self.drawRectangleWithCurvedCorner(canvas, x0, y0, x1, y1, 'topRight', oColor, fColor, width)
                elif (row, col) == (rows - 1, 0) : 
                    self.drawRectangleWithCurvedCorner(canvas, x0, y0, x1, y1, 'bottomLeft', oColor, fColor, width)
                elif (row, col) == (rows - 1, cols - 1) : 
                    self.drawRectangleWithCurvedCorner(canvas, x0, y0, x1, y1, 'bottomRight', oColor, fColor, width)
                else: 
                    canvas.create_rectangle(x0, y0, x1, y1, outline = oColor, width = width, fill = fColor)
                # color names from : http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
        
        self.drawDays(canvas)
        #self.drawStickers(canvas)

    # draws the dates
    def drawDays(self, canvas): 
        dateBoard = self.listOfMonthBoards[self.viewingMonth]
        cr = self.curveRadius
        rows, cols = self.rows[self.currentState], self.cols[self.currentState]
        for row in range(rows):
            for col in range(cols):
                x0, y0, x1, y1 = self.getCellBounds(row, col)
                date = str(dateBoard[row][col])
                if date == '-1': date = ''
            
                if self.mouseLocation == (row, col):
                    textSize = 18
                else: textSize = 12
                canvas.create_text(x1 - cr, y0 + cr, text = date, font = f'Courier {textSize} bold', fill = 'gray')

    # draws the back/next buttons
    def drawButtons(self, canvas):
        widthLeft = widthRight = 5
        textSizeLeft = textSizeRight = 30
        colorLeft = colorRight = 'lavender blush'

        if self.monthlyView:
            leftCondition = self.viewingMonth != 0
            rightCondition = self.viewingMonth != (len(self.months) - 1)
        elif self.dailyView:
            leftCondition = (self.viewingMonth, self.viewingDay) !=  (0, 1) 
            rightCondition = (self.viewingMonth, self.viewingDay) != (len(self.months) - 1, 31)
            

        if self.mouseInButtonLeft and leftCondition:
            widthLeft = 7
            textSizeLeft = 36
            colorLeft = 'mistyRose'
        
        elif self.mouseInButtonRight and rightCondition:
            widthRight = 7
            textSizeRight = 36
            colorRight = 'mistyRose'
        
        
        lx, rx = self.buttonLeftX, self.buttonRightX
        y = self.buttonY
        r = self.buttonRadius
        canvas.create_oval(lx + r , y + r, lx - r, y - r, outline = 'gray', width = widthLeft, fill = colorLeft)
        canvas.create_text(lx, y, text = '<', font = f'courier {textSizeLeft} bold', fill = 'gray')
        canvas.create_oval(rx + r, y + r, rx - r, y - r, outline = 'gray', width = widthRight, fill = colorRight)
        canvas.create_text(rx, y, text = '>', font = f'courier {textSizeRight} bold', fill = 'gray')

    # draws the weeks at the top (Sun through Sat)
    def drawWeeks(self, canvas):
        x0 = self.calX0
        y0 = self.calY0 - self.cellHeight // 4
        x1 = x0 + self.cellWidth
        y1 = self.calY0 

        for i in range(7):
            self.drawTabs(canvas, x0, y0, x1, y1, 20, 'gray', 2)
            x0, x1 = x1, x1 + self.cellWidth

        x = (self.calX0 + self.cellWidth//2)
        y = (self.calY0 - self.cellHeight//8)
        for week in self.weeks:
            canvas.create_text(x, y, text = week, font = 'Courier 12 bold', fill = 'white')
            x, y = x + self.cellWidth, y

    # draws the different headers for the different viewforms
    def drawHeader(self, canvas):
        
        cellWidth = self.gridWidth // self.cols[0]
        cellHeight = self.gridHeight // self.rows[0]

        if self.dailyView and self.mouseInHeader:
            width = 8
            color = 'mistyrose'
            textSize = 32
        else:
            width = 5
            color = 'lavender blush'
            textSize = 30


        self.drawRoundedRectangle(canvas, self.calX0 + cellWidth, self.calY0 - cellHeight, self.calX1 - cellWidth, self.calY0 - cellHeight/3, 
                                self.curveRadius, color, 'gray', width)

        month = self.months[self.viewingMonth] # changes with buttons
        bannerWidth = (self.calY0 - cellHeight/4) - (self.calY0 - cellHeight) 
        spacing = int(bannerWidth / len(month) // 4)
        formattedMonth = ''
        for char in month:
            formattedMonth += (char + (' ' * spacing))
        middleX = ((self.calX0 + cellWidth) + (self.calX1 - cellWidth)) // 2
        middleY = ((self.calY0 - cellHeight) + (self.calY0 - cellHeight/3)) // 2

        text = formattedMonth
        if self.dailyView:
            text = f'{formattedMonth}  {self.viewingDay}'
        canvas.create_text(middleX, middleY, text = text, font = f'Courier {textSize} bold', fill = 'gray')

    # draws the daily view
    def drawDailyView(self, canvas):
    
        # AM and PM
        monthCellHeight = self.gridHeight // self.rows[0]
        self.drawTabs(canvas, self.calX0, self.calY0 - monthCellHeight // 4, self.calX0 + self.cellWidth//2, self.calY0, 
                      self.curveRadius, 'gray', width = 3)
        canvas.create_text(((self.calX0) + (self.calX0 +self.cellWidth//2))//2, ((self.calY0 - monthCellHeight // 4) + (self.calY0))//2, 
                          text = 'A . M .', font = 'courier 18 bold', fill = 'white')
        self.drawTabs(canvas, self.calX0 + self.cellWidth//2, self.calY0 - monthCellHeight // 4, self.calX0 + self.cellWidth, self.calY0, 
                      self.curveRadius, 'gray', width = 3)
        canvas.create_text(((self.calX0 +self.cellWidth//2) + (self.calX0 + self.cellWidth))//2, ((self.calY0 - monthCellHeight // 4) + (self.calY0))//2, 
                          text = 'P . M .', font = 'courier 18 bold', fill = 'white')

        # divider
        canvas.create_line(self.width//2, self.calY0, self.width//2, self.calY1, fill = 'gray', width = 4)

        # time lines
        dy = (self.calY1 - self.calY0)//12
        for i in range(1, 13):
            canvas.create_line(self.calX0 + 5, self.calY0 + i*dy, self.calX1 - 5, self.calY0 + i*dy, fill = 'gray', width = 2)
        # a.m.
        for i in range(1, 13):
            canvas.create_text(self.calX0 + 8, self.calY0 + i*dy - 8, text = f'{i}:00', font = 'Courier 12 italic', fill = 'gray', anchor = W)
        # p.m.
        for i in range(1, 13):
            canvas.create_text(self.width//2 + 8, self.calY0 + i*dy - 8, text = f'{i}:00', font = 'Courier 12 italic', fill = 'gray', anchor = W)

        self.drawPrediction(canvas)

        if self.viewingDay in self.listOfMonthEvents[self.viewingMonth]:
            self.drawPredeterminedEvents(canvas, self.viewingDay)

    # draws the predetermined events (courses, clubs, etc.)
    def drawPredeterminedEvents(self, canvas, day):
        month = self.listOfMonthEvents[self.viewingMonth]
        setOfEvents = month[day]
        for event in setOfEvents:
            listOfInfo = self.classes[event]

            beginningTime = listOfInfo[0]
            beginningHour, beginningMinutes = (beginningTime//100) % 100, beginningTime % 100
        
            endTime = listOfInfo[1]
            endHour, endMinutes = (endTime//100) % 100, endTime % 100
         
            margin = 75
            dy = (self.calY1 - self.calY0)//12
            ddy = dy//6 # increments of 10 minutes
            
            endY = self.calY1
            endY -= 5 # account for outline width

            # format the text for time
            text = self.createEventText(beginningHour, beginningMinutes, endHour, endMinutes, event)


            if beginningHour < 12 and endHour > 12:
                endHour %= 12
                x0, x1 = self.calX0 + margin, self.width//2 - margin
                x2, x3 = self.width//2 + margin, self.calX1 - margin
                y0, y1 = self.calY0 + (beginningHour * dy) + ((beginningMinutes//10) * ddy), endY
                y2, y3 = self.calY0, self.calY0 + (endHour * dy) + ((endMinutes//10) * ddy) 

                self.drawEvents(canvas, x0, y0, x1, y1, 'gray', 'mint cream', 3, text)
                self.drawEvents(canvas, x2, y2, x3, y3, 'gray', 'mint cream', 3, text)

            elif beginningHour < 12 and endHour <= 12:
                x0, x1 = self.calX0 + margin, self.width//2 - margin
                y0 = self.calY0 + (beginningHour * dy) + ((beginningMinutes//10) * ddy) 
                y1 = self.calY0 + (endHour * dy) + ((endMinutes//10) * ddy) 
                self.drawEvents(canvas, x0, y0, x1, y1, 'gray', 'mint cream', 3, text)

            elif beginningHour >= 12 and endHour >= 12:
                beginningHour %= 12
                endHour %= 12
                x0, x1 = self.width//2 + margin, self.calX1 - margin 
                y0 = self.calY0 + (beginningHour * dy) + ((beginningMinutes//10) * ddy)
                y1 = self.calY0 + (endHour * dy) + ((endMinutes//10) * ddy) 
                self.drawEvents(canvas, x0, y0, x1, y1, 'gray', 'mint cream', 3, text)

    # formats and creates the text that shows up on event blocks
    def createEventText(self, beginningHour, beginningMinutes, endHour, endMinutes, event):
        beginningHour = str(int(beginningHour%12))
        if beginningHour == '0': beginningHour = '12'
        if beginningMinutes == 0: beginningMinutes = '00'
        else: beginningMinutes = int(beginningMinutes)
        
        endHour = str(int(endHour%12))
        if endHour == '0': endHour = '12'
        if endMinutes == 0: endMinutes = '00'
        else: endMinutes = int(endMinutes)

        timeText = f'{beginningHour}:{beginningMinutes} - {endHour}:{endMinutes}'
        spacesToMiddle = ' ' * (len(event)//2 - len(timeText)//2)
        timeText = spacesToMiddle + timeText
        text = f'{timeText}\n{event}'
        return text
        
    # draws the event block
    def drawEvents(self, canvas, x0, y0, x1, y1, oColor, fColor, width, text):
        self.drawRoundedRectangle(canvas, x0, y0, x1, y1, self.curveRadius, fColor, oColor, width)
        dy = (self.calY1 - self.calY0)//24 # 30 minutes
        if y1 - y0 < dy:
            text.strip()
            tempList = text.split('\n')
            text = '\t'.join(tempList)
            textSize = 9
        else:
            textSize = 14

        midX = (x0 + x1)//2
        midY = (y0 + y1)//2
        canvas.create_text(midX, midY, text = text, font = f'courier {textSize} bold', fill = 'gray')

        
      

