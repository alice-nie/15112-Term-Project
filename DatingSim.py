# About this file: creates the dating sim mode for going to classes

from cmu_112_graphics import *
import datingSimClasses as char
from Room import *
# any quirky color names from http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
# all images drawn by Nhu Tat


class DatingSim(Mode):

    # intializes variables
    def appStarted(self):
        self.width, self.height = 1440, 778
        self.incrementX = self.width//5
        self.incrementY = self.height//10
        
        self.coverPage()
        self.mouseOverWillow = self.mouseOverKarl = self.mouseOverKimchee = self.mouseOverPaine = self.mouseOverCooper = False

        self.captureTargetImages()
        self.viewWillow = self.viewKarl = self.viewKimchee = self.viewPaine = self.viewCooper = False

        self.mouseOverDateBS = self.mouseOverDateMicroecon = self.mouseOverDate15112 = self.mouseOverDateCalc = self.mouseOverDateInterp = False
        self.mouseOverOk = False
        self.mouseInButton = False

        self.mouseOverGoBackToRoom = False

        self.dAffectionPoints = 0

    # any image alteration code learned from  https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html (used in room before)
    # intializes variables for the portraits
    def captureTargetImages(self):
        scaleSize = 1/3
        cooperHighlighted = self.loadImage('CooperHighlight.png')
        self.cooper = self.scaleImage(cooperHighlighted, scaleSize)
        karlHighlighted = self.loadImage('KarlHighlight.png')
        self.karl = self.scaleImage(karlHighlighted, scaleSize)
        kimcheeHighlighted = self.loadImage('KimcheeHighlight.png')
        self.kimchee = self.scaleImage(kimcheeHighlighted, scaleSize)
        paineHighlighted = self.loadImage('PaineHighlight.png')
        self.paine = self.scaleImage(paineHighlighted, scaleSize)
        willowHighlighted = self.loadImage('WillowHighlight.png')
        self.willow = self.scaleImage(willowHighlighted, scaleSize)
        self.captureTargetWidth, self.captureTargetHeight = self.cooper.size

    # intializes variables for the background/cover page
    def coverPage(self):
        scaleSize = 1/2
        cooper = self.loadImage('Cooper.png')
        cooper = self.scaleImage(cooper, scaleSize) 
        karl = self.loadImage('Karl.png')
        karl = self.scaleImage(karl, scaleSize)
        kimchee = self.loadImage('Kimchee.png')
        kimchee = self.scaleImage(kimchee, scaleSize)
        paine = self.loadImage('Paine.png')
        paine = self.scaleImage(paine, scaleSize)
        willow = self.loadImage('Willow.png')
        willow = self.scaleImage(willow, scaleSize)
        
        coverWidth, coverHeight = cooper.size #512, 875
        desiredWidth, desiredHeight = self.width // 5, self.height # 288, 788
        cropX0, cropY0 = (coverWidth - desiredWidth)/2, (coverHeight - desiredHeight)/2
        cropX1, cropY1 = cropX0 + desiredWidth, cropY0 + desiredHeight
        

        # Code for changing pixel colors taken from https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html
        self.cooperCover = cooper.crop((cropX0, cropY0, cropX1, cropY1))
        cooperCover = self.cooperCover.convert('RGB')
        self.cooperCoverDim = Image.new(mode='RGB', size=cooperCover.size)
        for x in range(self.cooperCoverDim.width):
            for y in range(self.cooperCoverDim.height):
                r,g,b = cooperCover.getpixel((x,y))
                self.cooperCoverDim.putpixel((x,y),(r//2,g//2,b//2))
        
        self.karlCover = karl.crop((cropX0, cropY0, cropX1, cropY1))
        karlCover = self.karlCover.convert('RGB')
        self.karlCoverDim = Image.new(mode='RGB', size=karlCover.size)
        for x in range(self.karlCoverDim.width):
            for y in range(self.karlCoverDim.height):
                r,g,b = karlCover.getpixel((x,y))
                self.karlCoverDim.putpixel((x,y),(r//2,g//2,b//2))
        
        self.kimcheeCover = kimchee.crop((cropX0, cropY0, cropX1, cropY1))
        kimcheeCover = self.kimcheeCover.convert('RGB')
        self.kimcheeCoverDim = Image.new(mode='RGB', size=kimcheeCover.size)
        for x in range(self.kimcheeCoverDim.width):
            for y in range(self.kimcheeCoverDim.height):
                r,g,b = kimcheeCover.getpixel((x,y))
                self.kimcheeCoverDim.putpixel((x,y),(r//2,g//2,b//2))
        
        self.paineCover = paine.crop((cropX0, cropY0, cropX1, cropY1))
        paineCover = self.paineCover.convert('RGB')
        self.paineCoverDim = Image.new(mode='RGB', size=paineCover.size)
        for x in range(self.paineCoverDim.width):
            for y in range(self.paineCoverDim.height):
                r,g,b = paineCover.getpixel((x,y))
                self.paineCoverDim.putpixel((x,y),(r//2,g//2,b//2))

        self.willowCover = willow.crop((cropX0, cropY0, cropX1, cropY1))
        willowCover = self.willowCover.convert('RGB')
        self.willowCoverDim = Image.new(mode='RGB', size=willowCover.size)
        for x in range(self.willowCoverDim.width):
            for y in range(self.willowCoverDim.height):
                r,g,b = willowCover.getpixel((x,y))
                self.willowCoverDim.putpixel((x,y),(r//2,g//2,b//2))
        
###########################################################################

    
    # distance formula
    def distance(self, x0, y0, x1, y1):
        return ((x0 - x1) ** 2 + (y0 - y1) ** 2) ** 0.5

    # tracks mouse movement
    def mouseMoved(self, event):
        if not self.viewWillow and not self.viewKarl and not self.viewKimchee and not self.viewPaine and not self.viewCooper:
            if 0 < event.x < self.width//2 - 1.5*self.incrementX: self.mouseOverWillow = True
            else: self.mouseOverWillow = False
            if self.width//2 - 1.5*self.incrementX < event.x < self.width//2 - 0.5*self.incrementX: self.mouseOverKarl = True
            else: self.mouseOverKarl = False
            if self.width//2 - 0.5*self.incrementX < event.x < self.width//2 + 0.5*self.incrementX: self.mouseOverKimchee = True
            else: self.mouseOverKimchee = False
            if self.width//2 + 0.5*self.incrementX < event.x < self.width//2 + 1.5*self.incrementX: self.mouseOverPaine = True
            else: self.mouseOverPaine = False
            if self.width//2 + 1.5*self.incrementX < event.x < self.width: self.mouseOverCooper = True
            else: self.mouseOverCooper = False
        
        mouseInButton = (self.width//2 + 1.4*self.incrementX <=  event.x <= self.width//2 + 1.4*self.incrementX + self.incrementX//2 and 
                        self.height//2 - 4.5*self.incrementY < event.y < self.height//2 - 4.5*self.incrementY + self.incrementY)
        self.mouseInButton = mouseInButton
        if self.viewWillow and self.mouseInButton: self.mouseOverDateBS = True
        else: self.mouseOverDateBs = False
        if self.viewKarl and self.mouseInButton: self.mouseOverDateMicroecon = True
        else: self.mouseOverDateMicroecon = False
        if self.viewKimchee and self.mouseInButton: self.mouseOverDate15112 = True
        else: self.mouseOverDate15112 = False
        if self.viewPaine and self.mouseInButton: self.mouseOverDateCalc = True
        else: self.mouseOverDateCalc = False
        if self.viewCooper and self.mouseInButton: self.mouseOverDateInterp = True
        else: self.mouseOverDateInterp = False


        if self.viewWillow or self.viewKarl or self.viewKimchee or self.viewPaine or self.viewCooper: # and class in session
            if (self.width//2 + .1*self.incrementX <= event.x <= self.width//2 + .1*self.incrementX + self.incrementX//2 and
                self.height//2 - 4.5*self.incrementY < event.y < self.height//2 - 4.5*self.incrementY + self.incrementY):
                self.mouseOverGoBackToRoom = True
            else: self.mouseOverGoBackToRoom = False


        y1 = self.height//2 + self.captureTargetHeight//4 - (self.captureTargetHeight//2)//5
        if (self.distance(event.x, event.y, self.width//2, y1) <= 20 and 
            (char.BS.attendedClass or char.BS.attendedClassTardy or char.Microecon.attendedClass or char.Microecon.attendedClassTardy or char.Cs15112.attendedClass or 
            char.Cs15112.attendedClassTardy or char.Calc.attendedClass or char.Calc.attendedClassTardy or char.Interp.attendedClass or char.Interp.attendedClassTardy)):
            self.mouseOverOk = True
        else: self.mouseOverOk = False
    
    # performs action based on where mouse is pressed -- mainly points for attending class
    def mousePressed(self, event):
        
        if event.x < self.width//2 - self.incrementX or event.x > self.width//2 + 2*self.incrementX:
            if self.viewWillow: self.viewWillow = False
            elif self.viewKarl: self.viewKarl = False
            elif self.viewKimchee: self.viewKimchee = False
            elif self.viewPaine: self.viewPaine = False
            elif self.viewCooper: self.viewCooper = False
        
        # view profiles
        if self.mouseOverWillow: self.viewWillow, self.mouseOverWillow = True, False
        elif self.mouseOverKarl: self.viewKarl, self.mouseOverKarl = True, False
        elif self.mouseOverKimchee: self.viewKimchee, self.mouseOverKimchee = True, False
        elif self.mouseOverPaine: self.viewPaine, self.mouseOverPaine = True, False
        elif self.mouseOverCooper: self.viewCooper, self.mouseOverCooper = True, False

      
        if self.mouseOverDateBS:
            if char.player.meals + char.player.soldMeals != 1:
                char.player.eatOrSell = True
                self.app.setActiveMode(self.room)
                return
            oldAffectionPoints = char.BS.affectionPoints
            if char.BS.classTime: 
                char.BS.attendedClass = True
                char.BS.addDatePoints(1, 20)
                char.player.freeHoursLeft -= 1 + char.Alice.round(20/6)
            elif char.BS.classTimeTardy: 
                oldAffectionPoints = char.BS.affectionPoints
                char.BS.attendedClassTardy = True
                char.player.freeHoursLeft -= char.Alice.round(60 - (char.player.currentMinute/60)) + 1
                char.BS.addDatePoints(1, 60 - char.player.currentMinute)
            self.dAffectionPoints = char.Alice.round(char.BS.affectionPoints - oldAffectionPoints)
            
        elif self.mouseOverDateMicroecon:
            if char.player.meals + char.player.soldMeals != 1:
                char.player.eatOrSell = True
                self.app.setActiveMode(self.app.room)
                return
            oldAffectionPoints = char.Microecon.affectionPoints
            if char.Microecon.classTime: 
                char.Microecon.attendedClass = True
                char.Microecon.addDatePoints(0, 50)
                char.player.freeHoursLeft -= round(50/60, 1)
            elif char.Microecon.classTimeTardy: 
                char.Microecon.attendedClassTardy = True
                char.player.freeHoursLeft -= round((50 - char.player.currentMinute)/60, 1)
                char.Microecon.addDatePoints(0, 50 - char.player.currentMinute)
            self.dAffectionPoints = char.Alice.round(char.Microecon.affectionPoints - oldAffectionPoints)

        elif self.mouseOverDate15112:
            if char.player.meals + char.player.soldMeals != 2 and char.player.currentWeek != 6:
                char.player.eatOrSell = True
                self.app.setActiveMode(self.app.room)
                return
            oldAffectionPoints = char.Cs15112.affectionPoints
            if char.Cs15112.classTime: 
                char.Cs15112.attendedClass = True
                char.Cs15112.addDatePoints(1, 20)
                char.player.freeHoursLeft -= 1 + round(20/60, 1)
            elif char.Cs15112.classTimeTardy: 
                char.Cs15112.attendedClassTardy = True
                char.player.freeHoursLeft -=  round((60 - char.player.currentMinute)/60, 1) + round(40/60, 1)
                char.Cs15112.addDatePoints(0, (60 - char.player.currentMinute + 40)) # tardy + end
            elif char.Cs15112.recitation:
                char.Cs15112.attendedClass = True
                char.Cs15112.addDatePoints(0, 50)
                char.player.freeHoursLeft -= round(50/60, 1)
            elif char.Cs15112.recitationTardy:
                char.Cs15112.attendedClass = True
                char.player.freeHoursLeft -=  round((50 - char.player.currentMinute)/60, 1) 
                char.Cs15112.addDatePoints(0, 50 - char.player.currentMinute)
            elif char.Cs15112.collab:
                char.Cs15112.attendedClass = True
                char.Cs15112.addDatePoints(3, 0)
                char.player.freeHoursLeft -= 3
            self.dAffectionPoints = char.Alice.round(char.Cs15112.affectionPoints - oldAffectionPoints)
            
        elif self.mouseOverDateCalc:
            if char.player.currentWeek == 2 and char.player.meals + char.player.soldMeals != 2:
                char.player.eatOrSell = True
                self.app.setActiveMode(self.app.room)
                return
            oldAffectionPoints = char.Calc.affectionPoints
            if char.Calc.classTime: 
                char.Calc.attendedClass = True
                char.Calc.addDatePoints(0, 50)
                char.player.freeHoursLeft -= char.Alice.round(50/60)
            elif char.Calc.classTimeTardy: 
                char.Calc.attendedClassTardy = True
                char.player.freeHoursLeft -= char.Alice.round((60 - char.player.currentMinute)/60) + char.ALice.round(10/60)
                char.player.addDatePoints(0, 60 - char.player.currentMinute + 10)
            self.dAffectionPoints = char.Alice.round(char.Calc.affectionPoints - oldAffectionPoints)
            
        elif self.mouseOverDateInterp:
            if char.player.meals + char.player.soldMeals != 2:
                char.player.eatOrSell = True
                self.app.setActiveMode(self.app.room)
                return
            oldAffectionPoints = char.Interp.affectionPoints
            if char.Interp.classTime: 
                char.Interp.attendedClass = True
                char.Interp.addDatePoints(0, 50)
                char.player.freeHoursLeft -= round(50/60, 1)
            elif char.Interp.classTimeTardy: 
                char.Interp.attendedClassTardy = True
                char.player.freeHoursLeft -= round((60 - char.player.currentMinute)/60, 1) + round(10/60, 1)
                char.player.addDatePoints(0, 60 - char.player.currentMinute + 10)
            self.dAffectionPoints = round(char.Interp.affectionPoints - oldAffectionPoints, 1)
            

        if self.mouseOverOk:
            # reset for next time
            self.viewWillow = self.viewKarl = self.viewKimchee = self.viewPaine = self.viewCooper = self.wentToClass = False
            self.app.setActiveMode(self.app.room)
            self.mouseOverOk = False
            char.Cs15112.classTime = char.Microecon.classTime = char.Calc.classTime = char.Interp.classTime = char.BS.classTime = False
            char.Cs15112.classTimeTardy = char.Microecon.classTimeTardy = char.Calc.classTimeTardy = char.Interp.classTimeTardy = char.BS.classTimeTardy = False
            char.BS.attendedClass = char.BS.attendedClassTardy = char.Microecon.attendedClass = char.Microecon.attendedClassTardy = char.Cs15112.attendedClass = char.Cs15112.attendedClassTardy  = char.Calc.attendedClass = char.Calc.attendedClassTardy = char.Interp.attendedClasss = char.Interp.attendedClassTardy = False
            self.mouseInButton = False


        if self.mouseOverGoBackToRoom:
            self.viewWillow = self.viewKarl = self.viewKimchee = self.viewPaine = self.viewCooper = self.wentToClass = False
            self.app.setActiveMode(self.app.room)
            self.mouseOverGoBackToRoom = False
            char.Cs15112.classTime = char.Microecon.classTime = char.Calc.classTime = char.Interp.classTime = char.BS.classTime = False
            char.Cs15112.classTimeTardy = char.Microecon.classTimeTardy = char.Calc.classTimeTardy = char.Interp.classTimeTardy = char.BS.classTimeTardy = False

    # code taken from https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html
    # caches images
    def getCachedPhotoImage(self, image):
        # stores a cached version of the PhotoImage in the PIL/Pillow image
        if ('cachedPhotoImage' not in image.__dict__):
            image.cachedPhotoImage = ImageTk.PhotoImage(image)
        return image.cachedPhotoImage
        

###########################################################################
    
    # draws everything
    def redrawAll(self, canvas):
        self.drawCover(canvas)
        if self.viewWillow:
            self.drawWillow(canvas)
        elif self.viewKarl:
            self.drawKarl(canvas)
        elif self.viewKimchee:
            self.drawKimchee(canvas)
        elif self.viewPaine:
            self.drawPaine(canvas)
        elif self.viewCooper:
            self.drawCooper(canvas)
        
        if (char.BS.attendedClass or char.BS.attendedClassTardy or char.Microecon.attendedClass or char.Microecon.attendedClassTardy or char.Cs15112.attendedClass or char.Cs15112.attendedClassTardy 
            or char.Calc.attendedClass or char.Calc.attendedClassTardy or char.Interp.attendedClass or char.Interp.attendedClassTardy):
            self.drawWentToClassPopUp(canvas)

    # draws the cover/background
    def drawCover(self, canvas):
        # following code (about cached images) from https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html

        incrementX, incrementY = self.incrementX, self.incrementY
        if self.mouseOverWillow: image1 = self.getCachedPhotoImage(self.willowCover)
        else: image1 = self.getCachedPhotoImage(self.willowCoverDim)
        if self.mouseOverKarl: image2 = self.getCachedPhotoImage(self.karlCover)
        else: image2 = self.getCachedPhotoImage(self.karlCoverDim)
        if self.mouseOverKimchee: image3 = self.getCachedPhotoImage(self.kimcheeCover)
        else: image3 = self.getCachedPhotoImage(self.kimcheeCoverDim)
        if self.mouseOverPaine: image4 = self.getCachedPhotoImage(self.paineCover)
        else: image4 = self.getCachedPhotoImage(self.paineCoverDim)
        if self.mouseOverCooper: image5 = self.getCachedPhotoImage(self.cooperCover)
        else: image5 = self.getCachedPhotoImage(self.cooperCoverDim)

        canvas.create_image(self.width//2 - 2*incrementX, self.height//2, image = image1)
        canvas.create_line(self.width//2 - 1.5*incrementX, 0, self.width//2 - 1.5*incrementX, self.height, width = 15, fill = 'black')
        canvas.create_image(self.width//2 - incrementX, self.height//2, image = image2)
        canvas.create_line(self.width//2 - 0.5*incrementX, 0, self.width//2 - 0.5*incrementX, self.height, width = 15, fill = 'black')
        canvas.create_image(self.width//2, self.height//2 , image = image3)
        canvas.create_line(self.width//2 + 0.5*incrementX, 0, self.width//2 + 0.5*incrementX, self.height, width = 15, fill = 'black')
        canvas.create_image(self.width//2 + incrementX, self.height//2, image = image4)
        canvas.create_line(self.width//2 + 1.5*incrementX, 0, self.width//2 + 1.5*incrementX, self.height, width = 15, fill = 'black')
        canvas.create_image(self.width//2 + 2*incrementX, self.height//2, image = image5)

    # draws BS
    def drawWillow(self, canvas):
        x, y = self.width//2 - self.incrementX, self.height//2 - self.incrementY
        canvas.create_image(x, y, image = ImageTk.PhotoImage(self.willow))
        self.drawWillowAffectionBar(canvas)

        # profile
        x0, y0 = x + self.incrementX, self.height//2 - self.incrementY - self.captureTargetHeight//2
        x1, y1 = x + 3*self.incrementX, self.height - self.incrementY//2
        self.drawRoundedRectangle(canvas, x0, y0, x1, y1, 20, 'burlywood2', 'black', 5)

        margin = 20
        space = 60
        x = x0 + margin
        y = y0 + space
        canvas.create_text((x0 + x1)//2, y, text = 'Profile', font = 'courier 30 bold underline', fill = 'black')
        lines = ['Name: Willow', 
                '''Height / Weight: 5'11'' / 150 lbs ''', 
                'Date of Birth: National Gerbil Day', 
                'Blood type: O', 
                'Favorite food: Anything from a food truck', 
                'Skills: Zoom vfx',
                'Personality: Easygoing',
                '''Quote:\n"Sometimes I feel like I'm going insane"''',
                '',
                'Other notes: N/A']
        y += space
        for i in range(len(lines)):
            canvas.create_text(x, y + i*space, anchor = NW, text = lines[i], font = 'courier 20', fill = 'black')

        if char.BS.classTime or char.BS.classTimeTardy: classTime = True
        else: classTime = False
        self.drawGoToClass(canvas, self.mouseOverDateBS, classTime)
        self.drawGoBackToRoom(canvas)

    # draws Microecon
    def drawKarl(self, canvas):
        x, y = self.width//2 - self.incrementX, self.height//2 - self.incrementY
        canvas.create_image(x, y, image = ImageTk.PhotoImage(self.karl))
        self.drawKarlAffectionBar(canvas)

        # profile
        x0, y0 = x + self.incrementX, self.height//2 - self.incrementY - self.captureTargetHeight//2
        x1, y1 = x + 3*self.incrementX, self.height - self.incrementY//2
        self.drawRoundedRectangle(canvas, x0, y0, x1, y1, 20, 'salmon', 'black', 5)

        margin = 20
        space = 60
        x = x0 + margin
        y = y0 + space
        canvas.create_text((x0 + x1)//2, y, text = 'Profile', font = 'courier 30 bold underline', fill = 'black')
        lines = ['Name: Karl', 
                '''Height / Weight: 6'2'' / 160 lbs ''', 
                'Date of Birth: 6/19', # national money day
                'Blood type: A', 
                'Favorite food: Money', 
                'Skills: Making graphs out of everything',
                'Personality: Confusing',
                '''Quote: "m a r g i n a l"''',
                'Other notes:\nRather hard to understand at times']
        y += space
        for i in range(len(lines)):
            canvas.create_text(x, y + i*space, anchor = NW, text = lines[i], font = 'Courier 20', fill = 'black')

        if char.Microecon.classTime or char.Microecon.classTimeTardy: classTime = True
        else: classTime = False
        self.drawGoToClass(canvas, self.mouseOverDateMicroecon, classTime)
        
        self.drawGoBackToRoom(canvas)

    # draws CS
    def drawKimchee(self, canvas):
        x, y = self.width//2 - self.incrementX, self.height//2 - self.incrementY
        canvas.create_image(x, y, image = ImageTk.PhotoImage(self.kimchee))
        self.drawKimcheeAffectionBar(canvas)

        # profile
        x0, y0 = x + self.incrementX, self.height//2 - self.incrementY - self.captureTargetHeight//2
        x1, y1 = x + 3*self.incrementX, self.height - self.incrementY//2
        self.drawRoundedRectangle(canvas, x0, y0, x1, y1, 20, 'khaki1', 'black', 5)

        margin = 20
        space = 60
        x = x0 + margin
        y = y0 + space
        canvas.create_text((x0 + x1)//2, y, text = 'Profile', font = 'courier 30 bold underline', fill = 'black')
        lines = ['Name: Kimchee', 
                '''Height / Weight: 1'5'' / 112 lbs ''', 
                'Date of Birth: 8/20', # national axolotl day
                'Blood type: AB', 
                "Favorite food: idk computers?", 
                'Skills: Very motivating emails',
                'Personality: Needs a lot of attention',
                '''Quote:\n"You don't need any prior coding experience"''',
                'Other notes: Looks like a vampire.\nKnown to suck the life out of people.']
        y += space
        for i in range(len(lines)):
            canvas.create_text(x, y + i*space, anchor = NW, text = lines[i], font = 'Courier 20', fill = 'black')

        if char.Cs15112.classTime or char.Cs15112.classTimeTardy or char.Cs15112.recitation or char.Cs15112.recitationTardy or char.Cs15112.collab: classTime = True
        else: classTime = False
        self.drawGoToClass(canvas, self.mouseOverDate15112, classTime)
        self.drawGoBackToRoom(canvas)

    # draws Calc
    def drawPaine(self, canvas):
        x, y = self.width//2 - self.incrementX, self.height//2 - self.incrementY
        canvas.create_image(x, y, image = ImageTk.PhotoImage(self.paine))
        self.drawPaineAffectionBar(canvas)

        # profile
        x0, y0 = x + self.incrementX, self.height//2 - self.incrementY - self.captureTargetHeight//2
        x1, y1 = x + 3*self.incrementX, self.height - self.incrementY//2
        self.drawRoundedRectangle(canvas, x0, y0, x1, y1, 20, 'cornflower blue', 'black', 5)

        margin = 20
        space = 60
        x = x0 + margin
        y = y0 + space
        canvas.create_text((x0 + x1)//2, y, text = 'Profile', font = 'courier 30 bold underline', fill = 'black')
        lines = ['Name: Paine', 
                '''Height / Weight: 6'0'' / too heavy to carry ''', 
                'Date of Birth: 1/27',  # national sad day
                'Blood type: F', 
                "Favorite food: My tears", 
                'Skills: Creating the longest homeworks',
                'Personality: Spain without the S.',
                '''Quote: "10 hours per week"''',
                'Other notes: Send help.']
        y += space
        for i in range(len(lines)):
            canvas.create_text(x, y + i*space, anchor = NW, text = lines[i], font = 'Courier 20', fill = 'black')

        if char.Calc.classTime or char.Calc.classTimeTardy: classTime = True
        else: classTime = False
        self.drawGoToClass(canvas, self.mouseOverDateCalc, classTime)
        self.drawGoBackToRoom(canvas)

    # draws Interp
    def drawCooper(self, canvas):
        x, y = self.width//2 - self.incrementX, self.height//2 - self.incrementY
        canvas.create_image(x, y, image = ImageTk.PhotoImage(self.cooper))
        self.drawCooperAffectionBar(canvas)

        # profile
        x0, y0 = x + self.incrementX, self.height//2 - self.incrementY - self.captureTargetHeight//2
        x1, y1 = x + 3*self.incrementX, self.height - self.incrementY//2
        self.drawRoundedRectangle(canvas, x0, y0, x1, y1, 20, 'plum2', 'black', 5)

        margin = 20
        space = 60
        x = x0 + margin
        y = y0 + space
        canvas.create_text((x0 + x1)//2, y, text = 'Profile', font = 'courier 30 bold underline', fill = 'black')
        lines = ['Name: Cooper', 
                '''Height / Weight: 5'10'' / 150 ''', 
                'Date of Birth: 9/12',  # national video game day
                'Blood type: O', 
                "Favorite food: Butterscotch Pie", 
                'Skills: Playing video games',
                'Personality: Fun, Kind, Caring\neverything good in this world',
                '''Quote:\n"furries are the least of our problems"''',
                'Other notes: Literally best boy.']
        y += space
        for i in range(len(lines)):
            canvas.create_text(x, y + i*space, anchor = NW, text = lines[i], font = 'Courier 20', fill = 'black')

        if char.Interp.classTime or char.Interp.classTimeTardy: classTime = True
        else: classTime = False
        self.drawGoToClass(canvas, self.mouseOverDateInterp, classTime)
        self.drawGoBackToRoom(canvas)

    # draws the capture targets
    def drawCaptureTargets(self, canvas):
        incrementX, incrementY = self.incrementX, self.incrementY
        canvas.create_image(self.width//2 - 2*incrementX, self.height//2 - incrementY, image = ImageTk.PhotoImage(self.willow))
        canvas.create_image(self.width//2 - incrementX, self.height//2 - incrementY, image = ImageTk.PhotoImage(self.karl))
        canvas.create_image(self.width//2, self.height//2 - incrementY, image = ImageTk.PhotoImage(self.kimchee))
        canvas.create_image(self.width//2 + incrementX, self.height//2 - incrementY, image = ImageTk.PhotoImage(self.paine))
        canvas.create_image(self.width//2 + 2*incrementX, self.height//2 - incrementY, image = ImageTk.PhotoImage(self.cooper))

    # draws BS lvl bar
    def drawWillowAffectionBar(self, canvas):
        fColor = 'burlywood2'
        cr = 10
        dx, dy = self.captureTargetWidth//2, 2*self.captureTargetHeight//5
        x0, y0, x1, y1 = self.width//2 - self.incrementX - dx , self.height//2 + dy, self.width//2 - self.incrementX + dx, self.height//2  + dy + 10
        barWidth = x1 - x0
        affectionPoints = barWidth / 500
        dx = char.BS.affectionPoints * affectionPoints
        if dx > 0:
            self.fillThinRoundedRectangle(canvas, x0, y0, x0 + dx, y1, cr, fColor, 0, True)
        self.drawThinRoundedRectangle(canvas, x0, y0, x1, y1, cr, fColor, 'white', 2, False)

        midX = (x0+x1)//2
        canvas.create_text(midX, y1 + self.incrementY//5, text = f'{char.Alice.round(char.BS.affectionPoints)} / 500', font = 'courier 12 bold', fill = 'white')

        # grade
        x, y, r = midX, y1 + dy//3, 40
        oColor = 'black'
        canvas.create_oval(x-r, y-r, x+r, y+r, fill = fColor, outline = oColor, width = 3)
        canvas.create_text(x, y, text = f'{char.BS.grade}', font = 'courier 30', fill = oColor)

    # Microecon lvl bar
    def drawKarlAffectionBar(self, canvas):
        fColor = 'salmon'
        cr = 10
        dx, dy = self.captureTargetWidth//2, 2*self.captureTargetHeight//5
        x0, y0, x1, y1 = self.width//2 - self.incrementX - dx , self.height//2 + dy, self.width//2 - self.incrementX + dx, self.height//2  + dy + 10
        barWidth = x1 - x0
        affectionPoints = barWidth / 500
        dx = char.Microecon.affectionPoints * affectionPoints
        if dx > 0:
            self.fillThinRoundedRectangle(canvas, x0, y0, x0 + dx, y1, cr, fColor, 0, True)
        self.drawThinRoundedRectangle(canvas, x0, y0, x1, y1, cr, fColor, 'white', 2, False)

        midX = (x0+x1)//2
        canvas.create_text(midX, y1 + self.incrementY//5, text = f'{char.Alice.round(char.Microecon.affectionPoints)} / 500', font = 'courier 12 bold', fill = 'white')

        # grade
        x, y, r = midX, y1 + dy//3, 40
        oColor = 'black'
        canvas.create_oval(x-r, y-r, x+r, y+r, fill = fColor, outline = oColor, width = 3)
        canvas.create_text(x, y, text = f'{char.Microecon.grade}', font = 'courier 30', fill = oColor)

    # CS lvl bar
    def drawKimcheeAffectionBar(self, canvas):
        fColor = 'khaki1'
        cr = 10
        dx, dy = self.captureTargetWidth//2, 2*self.captureTargetHeight//5
        x0, y0, x1, y1 = self.width//2 - self.incrementX - dx , self.height//2 + dy, self.width//2 - self.incrementX + dx, self.height//2  + dy + 10
        barWidth = x1 - x0
        affectionPoints = barWidth / 500
        dx = char.Cs15112.affectionPoints * affectionPoints
        if dx > 0:
            self.fillThinRoundedRectangle(canvas, x0, y0, x0 + dx, y1, cr, fColor, 0, True)
        self.drawThinRoundedRectangle(canvas, x0, y0, x1, y1, cr, fColor, 'white', 2, False)

        midX = (x0+x1)//2
        canvas.create_text(midX, y1 + self.incrementY//5, text = f'{char.Alice.round(char.Cs15112.affectionPoints)} / 500', font = 'courier 12 bold', fill = 'white')

        # grade
        x, y, r = midX, y1 + dy//3, 40
        oColor = 'black'
        canvas.create_oval(x-r, y-r, x+r, y+r, fill = fColor, outline = oColor, width = 3)
        canvas.create_text(x, y, text = f'{char.Cs15112.grade}', font = 'courier 30', fill = oColor)

    # Calc lvl bar
    def drawPaineAffectionBar(self, canvas):
        fColor = 'cornflower blue'
        cr = 10
        dx, dy = self.captureTargetWidth//2, 2*self.captureTargetHeight//5
        x0, y0, x1, y1 = self.width//2 - self.incrementX - dx , self.height//2 + dy, self.width//2 - self.incrementX + dx, self.height//2  + dy + 10
        barWidth = x1 - x0
        affectionPoints = barWidth / 500
        dx = char.Calc.affectionPoints * affectionPoints
        if dx > 0:
            self.fillThinRoundedRectangle(canvas, x0, y0, x0 + dx, y1, cr, fColor, 0, True)
        self.drawThinRoundedRectangle(canvas, x0, y0, x1, y1, cr, fColor, 'white', 2, False)

        midX = (x0+x1)//2
        canvas.create_text(midX, y1 + self.incrementY//5, text = f'{char.Alice.round(char.Calc.affectionPoints)} / 500', font = 'courier 12 bold', fill = 'white')

        # grade
        x, y, r = midX, y1 + dy//3, 40
        oColor = 'black'
        canvas.create_oval(x-r, y-r, x+r, y+r, fill = fColor, outline = oColor, width = 3)
        canvas.create_text(x, y, text = f'{char.Calc.grade}', font = 'courier 30', fill = oColor)

    # Interp lvl bar
    def drawCooperAffectionBar(self, canvas):
        fColor = 'plum2'
        cr = 10
        dx, dy = self.captureTargetWidth//2, 2*self.captureTargetHeight//5
        x0, y0, x1, y1 = self.width//2 - self.incrementX - dx , self.height//2 + dy, self.width//2 - self.incrementX + dx, self.height//2  + dy + 10
        barWidth = x1 - x0
        affectionPoints = barWidth / 500
        dx = char.Interp.affectionPoints * affectionPoints
        if dx > 0:
            self.fillThinRoundedRectangle(canvas, x0, y0, x0 + dx, y1, cr, fColor, 0, True)
        self.drawThinRoundedRectangle(canvas, x0, y0, x1, y1, cr, fColor, 'white', 2, False)

        midX = (x0+x1)//2
        canvas.create_text(midX, y1 + self.incrementY//5, text = f'{char.Alice.round(char.Interp.affectionPoints)} / 500', font = 'courier 12 bold', fill = 'white')

        # grade
        x, y, r = midX, y1 + dy//3, 40
        oColor = 'black'
        canvas.create_oval(x-r, y-r, x+r, y+r, fill = fColor, outline = oColor, width = 3)
        canvas.create_text(x, y, text = f'{char.Interp.grade}', font = 'courier 30', fill = oColor)

    # draws the go to class button
    def drawGoToClass(self, canvas, mouseOver, classTime):
        if (mouseOver and classTime): 
            fill = True
            textSize = 22
            width = 5
        else: 
            fill = False
            textSize = 20
            width = 3
        x0, y0 = self.width//2 + 1.4*self.incrementX, self.height//2 - 4.5*self.incrementY
        x1, y1 = x0 + self.incrementX//2, y0 + self.incrementY
        self.drawRoundedRectangle(canvas, x0, y0, x1, y1, 20, 'light grey', 'black', width, fill)
        midX = (x0 + x1)//2
        midY = (y0 + y1)//2
        canvas.create_text(midX, midY, text = 'Go on\na date', font = f'Courier {textSize} italic', fill = 'black')

    # draws the go back to room button
    def drawGoBackToRoom(self, canvas):
        if self.mouseOverGoBackToRoom: 
            fill = True
            textSize = 22
            width = 5
        else: 
            fill = False
            textSize = 20
            width = 3
        x0, y0 = self.width//2 + .1*self.incrementX, self.height//2 - 4.5*self.incrementY
        x1, y1 = x0 + self.incrementX//2, y0 + self.incrementY
        self.drawRoundedRectangle(canvas, x0, y0, x1, y1, 20, 'light grey', 'black', width, fill)
        midX = (x0 + x1)//2
        midY = (y0 + y1)//2
        canvas.create_text(midX, midY, text = 'Go back\nto room', font = f'Courier {textSize} italic', fill = 'black')

    # draws attendance confirmation
    def drawWentToClassPopUp(self, canvas):
        x0, y0 = self.width//2 - self.captureTargetWidth, self.height//2 - self.captureTargetHeight//4
        x1, y1 = self.width//2 + self.captureTargetWidth, self.height//2 + self.captureTargetHeight//4
        self.drawRoundedRectangle(canvas, x0, y0, x1, y1, 20, 'light grey', 'black', 5, True)
        midX = (x0 + x1)/2
        midY = (y0 + y1)/2



        canvas.create_text(midX, midY, text = f'        You went on a date!\nYou got {self.dAffectionPoints} more affection points.', font = 'Courier 26 bold', fill = 'black')
        
        self.drawOk(canvas, x0, y0, x1, y1)

    # draws the OK text/button
    def drawOk(self, canvas, x0, y0, x1, y1):
        if self.mouseOverOk: color = 'salmon'
        else: color = 'black'
        midX = (x0 + x1)/2
        incrementY = (y1 - y0)//5
        y = y1 - incrementY
        canvas.create_text(midX, y, text = 'OK', font = 'Courier 26 bold', fill = color)


    # from Calendar

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
        #x0, x1 = self.width//2 - self.incrementX - self.captureTargetWidth//2, self.width//2 - self.incrementX + self.captureTargetWidth//2
        barWidth = self.captureTargetWidth
        affectionPoints = barWidth / 500
        dx = 20 * affectionPoints
        if fill == True:
            style = CHORD
            canvas.create_arc(x0, y0, x0 + 2*cr, y1, start = 90, extent = 180, style = style, fill = color, outline = color, width = width)
            if x1 - x0 >= dx:
                canvas.create_rectangle(x0 + cr, y0, x1 - cr, y1, fill = color, width = width)
                canvas.create_arc(x1 - 2*cr, y0, x1, y1, start = 270, extent = 180, style = style, fill = color, outline = color, width = width)

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


