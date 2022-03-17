
import random

# learned JSON from https://www.programiz.com/python-programming/json and https://opensource.com/article/19/7/save-and-load-data-python-json
import json

# the player
class Alice(object):
    
    # rounds to nearest tens place, with .05 going up
    @staticmethod
    def round(num):
        num *= 100
        if num % 10 >= 5:
            num += 10
        num //= 10
        num /= 10
        return num
        
    # initalizes variables for the player
    def __init__(self):

        self.name = 'Alice'
        self.currentPlayer = ''

        # track time
        self.currentHour = 9
        self.currentMinute = 0
        self.currentDay = 30
        self.currentMonth = 0 # 0 september, 1 october, 2 november, 3 december
        self.currentWeek = 3 # 0 sun, 1 mon, 2 tue, 3 wed, 4 thur, 5 fri, 6 sat
        self.resetDay()

        # statBars
        self.health = 90 # out of 100
        self.sleep = 0 # out of 8
        self.meals = 0 # out of 3
        self.productivity = 80 # out of 100
        self.stress = 50 # out of 100
        
        self.fun = 0 # "out of 3"

        # quota checks        
        self.showWarning = False
        self.warning = ''

        # for Calendar predictions:
        # each list represents a month, each element within the list is that day's productivity/sleep/meals/fun
        self.daysProductivity = [[80] * 29] + [[] for i in range(3)] 
        self.daysSleep = [[8] * 29] + [[] for i in range(3)]
        self.daysMeals = [[3] * 29] + [[] for i in range(3)]
        self.daysFun = [[180] * 29] + [[] for  i in range(3)]
        
        # each dictionary is a week (sun -> sat), keys are hours and values are a list of ('action', timeSpent)
        # changed keys to strings after reading https://stackoverflow.com/questions/17099556/why-do-int-keys-of-a-python-dict-turn-into-strings-when-using-json-dumps
        self.timeBlocks = [dict() for i in range(7)]
        for i in range(7):
            for j in range(0, 24):
                self.timeBlocks[i][str(j)] = list()


        # for JSON ("log-ins")
        try:
            # code from https://opensource.com/article/19/7/save-and-load-data-python-json
            accounts = open('accounts.txt')
            self.progress = json.load(accounts)
            accounts.close()
        except FileNotFoundError:
            self.progress = dict()
        
    # variables that reset day to day
    def resetDay(self):
        # 24hr time, day starts at 9 am
        self.freeHoursLeft = 10
        self.soldSleep = self.sleep = 0
        self.soldMeals = self.meals = 0
        self.soldFun = self.fun = 0
        self.timeToEat = [True, True, True]
        self.eatOrSell = False
        self.checkQuota = False
        
    # prints 'Alice'
    def __repr__(self):
        return f'{self.name}'

    # takes in hours; decrements health, increments sold sleep and free hours left 
    def sellSleep(self, hours):
        if self.soldSleep + self.sleep + hours <= 8:

            if (self.health - hours * 5) >= 0:
                self.health -= hours * 5
            else: self.health = 0

            self.soldSleep += hours
            self.freeHoursLeft += hours
        else:
            self.showWarning = True
            self.warning = f'You can only sell {8 - self.sleep - self.soldSleep}\nmore hour(s) of sleep'

    # sell 1 at a time; decrements health, increments sold meals and free hours left
    def sellMeal(self):
        if self.soldMeals + self.meals + 1 <= 3:

            if self.health - 7 >= 0:
                self.health -= 7
            else: self.health = 0

            self.soldMeals += 1
            self.freeHoursLeft += 1
        else:
            self.showWarning = True
            self.warning = f'You have no more meals to\nsell for today'

    # takes in minutes; decrements health, increments sold fun and free hours left 
    def sellFun(self, minutes):
        hours = Alice.round(minutes/60)
        if self.fun + self.soldFun + minutes <= 180: # 3 "required" hours 

            if self.health - hours * 5 >= 0:
                self.health -= hours * 5
            else: self.health = 0

            self.soldFun += minutes
            self.freeHoursLeft += hours
        else:
            self.showWarning = True
            self.warning = f'You can only sell {3 - self.fun - self.soldFun}\nmore minute(s) of\nrecommended fun time'

    # calculates health based on stress
    def calculateHealth(self):
        if self.stress > 50:
            self.health = random.randint(int(self.health - self.stress/20), int(self.health - self.stress/30))
        
        if self.health >= 100:
            self.health = 100
        elif self.health <= 0:
            self.health = 0

    # calculates the new time whenever an action is done
    def calculateNewTime(self, hours, minutes = 0, eating = False):

        ogHour, ogMinute = self.currentHour, self.currentMinute

        addHoursFromMinutes = (self.currentMinute + minutes) // 60
        self.currentMinute = (self.currentMinute + minutes) - 60*addHoursFromMinutes 
        self.currentHour = (self.currentHour + hours + addHoursFromMinutes) % 24

        if not eating:
            # first meal period: 9 am - 1 pm
            if ogHour < 13 <= self.currentHour or (13 - self.currentHour < 1):
                if self.meals + self.soldMeals != 1: 
                    self.currentHour, self.currentMinute = ogHour, ogMinute
                    self.eatOrSell = True
                    return

            # second meal period: 1 pm - 5 pm
            elif ogHour < 17 <= self.currentHour or (17 - self.currentHour < 1):
                if self.meals + self.soldMeals != 2:
                    self.currentHour, self.currentMinute = ogHour, ogMinute
                    self.eatOrSell = True
                    return

            # third meal period: 5 pm - 9 pm
            elif ogHour < 21 <= self.currentHour or (21 - self.currentHour < 1):     
                if self.meals + self.soldMeals != 3:
                    self.currentHour, self.currentMinute = ogHour, ogMinute
                    self.eatOrSell = True
                    return
        
        # new day
        if ogHour < 9 <= self.currentHour:

            # update attributes needed for prediction
            self.daysProductivity[self.currentMonth].append(self.productivity)
            self.daysSleep[self.currentMonth].append(self.sleep)
            self.daysMeals[self.currentMonth].append(self.meals)
            self.daysFun[self.currentMonth].append(self.fun)

            BS.timeSpentStudying[self.currentMonth].append(BS.studyingTimeToday)
            Microecon.timeSpentStudying[self.currentMonth].append(Microecon.studyingTimeToday)
            Cs15112.timeSpentStudying[self.currentMonth].append(Cs15112.studyingTimeToday)
            Calc.timeSpentStudying[self.currentMonth].append(Calc.studyingTimeToday)
            Interp.timeSpentStudying[self.currentMonth].append(Interp.studyingTimeToday)
             
            BS.studyingTimeToday = Microecon.studyingTimeToday = Cs15112.studyingTimeToday = Calc.studyingTimeToday = Interp.studyingTimeToday = 0
            
            self.resetDay()

        # past midnight
        if 0 <= self.currentHour < ogHour: 
            self.changeDate()
            self.currentWeek = (self.currentWeek + 1) % 7
        
        
        
        self.calculateStress()
        self.calculateProductivity()
        self.calculateHealth()

        # update the player's progress
        listOfStatKeys = ['health', 'stress', 'productivity', 'sleep', 'meals', 'currentHour', 'currentMinute', 'currentDay', 'currentMonth', 'currentWeek',
                                'daysProductivity', 'daysSleep', 'daysMeals', 'daysFun', 'timeBlocks']
        listOfStats = [self.health, self.stress, self.productivity, self.sleep, self.meals, self.currentHour, self.currentMinute, self.currentDay, self.currentMonth,
                        self.currentWeek, self.daysProductivity, self.daysSleep, self.daysMeals, self.daysFun, self.timeBlocks]
        for i in range(len(listOfStats)):
            self.progress[self.currentPlayer]['char.player.' + listOfStatKeys[i]] = listOfStats[i]
        
        # JSON code taken from https://www.programiz.com/python-programming/json
        with open('accounts.txt', 'w') as accounts:
            json.dump(self.progress, accounts)
            
    # updates date to next day
    def changeDate(self): 
        
        # no more school
        if (self.currentMonth == 4) and self.currentDay > 31:
            return

        self.currentDay += 1
        if (self.currentMonth == 0 or self.currentMonth == 2) and self.currentDay > 30: # max 30
            self.currentMonth += 1
            self.currentDay = 1
        elif (self.currentMonth == 1) and self.currentDay > 31:
            self.currentMonth += 1
            self.currentDay = 1

    # takes in hours; decrements stress and increments health and sleep (and free hours left if out of quota)
    def addSleep(self, hours):
        if self.sleep + self.soldSleep + hours <= 8:
            self.sleep += hours
        elif self.freeHoursLeft - hours >= 0:
            self.freeHoursLeft -= hours
        

        if (self.health + hours * 5) <= 100:
            self.health += hours * 5
        else: self.health = 100

        if (self.stress - hours * 3) >= 0:
            self.stress -= hours * 3
        else: self.stress = 0

        
        self.timeBlocks[self.currentWeek][str(self.currentHour)].append(('sleep', hours))
        self.calculateNewTime(hours)                                         
            
        if hours > 23:
            self.showWarning = True
            self.warning = f'bruh what'

    # eat 1 meal at a time; increments health and meals
    def eatMeal(self):
        if self.soldMeals + self.meals + 1 <= 3:
            
            if (self.health + 7) <= 100:
                self.health += 7
            else: self.health = 100

            self.meals += 1
            self.timeBlocks[self.currentWeek][str(self.currentHour)].append(('meal', 1))
            self.calculateNewTime(1, 0, True)

        else: 
            self.showWarning = True
            self.warning = 'No more meals for today :('

    # takes in minutes; decrements stress and increments health and fun (and free hours left if out of quota)
    def goOutside(self, minutes): 
        
        hours = Alice.round(minutes/60)
        
        if self.fun + self.soldFun + minutes <= 180:
            self.fun += minutes
        elif self.freeHoursLeft - hours >= 0:
            self.freeHoursLeft -= hours
        
        if (self.health + 2*hours) <= 100:
                self.health += 2*hours
        else: self.health = 100

        if (self.stress - hours * 3) >= 0:
                self.stress -= hours * 3
        else: self.stress = 0

        self.timeBlocks[self.currentWeek][str(self.currentHour)].append(('fun', minutes))
        self.calculateNewTime(0, minutes)
        
    # calculates productivity based on stress
    def calculateProductivity(self):
        productivity = self.productivity
        # depends on stress
        if self.stress > 50:
            productivity = random.randint(int(self.productivity - self.stress/10), int(self.productivity - self.stress/20))
        
        if self.health <= self.stress: self.productivity = min(50, productivity)
        else: self.productivity = productivity

        if self.productivity >= 100:
            self.productivity = 100
        elif self.productivity <= 0:
            self.productivity = 0
            
    # calculates stress based on productivity and sleep
    def calculateStress(self):
        stress = self.stress
        if self.productivity <= 40: stress += 2
        
        if self.sleep <= 4: self.stress = max(40, stress)
        else: self.stress = stress

        if self.stress >= 100:
            self.stress = 100
        elif self.stress <= 0:
            self.stress = 0
            

player = Alice()



class captureTarget(object):

    # intializes variables
    def __init__(self, name):
        self.name = name

        # otome elements
        self.affectionPoints = 0 # 100 per grade
        self.grade = 'F' # 5 grades, A, B, C, D, F

        self.noTime = False
        self.difficultyLevel = 0 # 0 to 4

        # date 
        self.classTime = self.classTimeTardy = False
        self.recitation = self.recitationTardy = self.collab = False # for 15112
        self.attendedClass = self.attendedClassTardy = False

        # for Calendar predictions
        # each list represents a month, each element within the list is that day's time spent studying
        self.studyingTimeToday = 0
        self.timeSpentStudying = [[60] * 29] + [[] for i in range(3)] 

    # prints capture target's name
    def __repr__(self):
        return f'{self.name}'

    # calculates the affection points for studying depending on productivity, difficulty, and time
    def addStudyPoints(self, minutes):
        difficulty = self.difficultyLevel + 1
        hours = Alice.round(minutes/60)

        if player.freeHoursLeft - hours < 0:
            self.noTime = True
            player.checkQuota = True
            return

        self.affectionPoints = min( 500, self.affectionPoints + Alice.round( (5 / (difficulty/2)) * hours * (player.productivity/70)) )

        if hours >= 3: player.stress + 7*hours
        else: player.stress += Alice.round(5 * (difficulty/6) * hours)

        player.health -= difficulty
    
        player.timeBlocks[player.currentWeek][str(player.currentHour)].append(('study', minutes))
        player.calculateNewTime(0, minutes)
        player.freeHoursLeft -= hours
        self.studyingTimeToday += minutes
        self.calculateGrade()

    # Calculates grade (100 affection points per grade)
    def calculateGrade(self):
        self.grade = ['F', 'D', 'C', 'B', 'A'][min(int(self.affectionPoints / 100), 4)]

    # calculates the points for going to class based on class difficulty and productivity
    def addDatePoints(self, hours, minutes):
        difficulty = self.difficultyLevel + 2
        if self.attendedClass: self.affectionPoints += Alice.round( 10 / (difficulty/2) * (player.productivity/50))
        elif self.attendedClassTardy: self.affectionPoints += Alice.round( 10 / (difficulty/4) * (player.productivity/50))
        player.calculateNewTime(hours, minutes)



BS = captureTarget('Willow')
BS.difficultyLevel = 1

Microecon = captureTarget('Karl')
Microecon.difficultyLevel = 2

Cs15112 = captureTarget('Kimchee')
Cs15112.difficultyLevel = 3

Calc = captureTarget('Paine')
Calc.difficultyLevel = 4

Interp = captureTarget('Cooper')
Interp.difficultyLevel = 0




