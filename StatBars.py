from cmu_112_graphics import *

import datingSimClasses as char
# any quirky color names from http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter


class StatBars(Mode):
    # BARS  
    def appStarted(self):

        # for importing
        self.width, self.height = 1440, 778

        # some info from omniBox
        self.incrementX = self.width//15
        self.incrementY = self.height//10
        #self.x0, self.y0 = self.width - (6*self.incrementX), self.height - (5*self.incrementY)
        #self.x1, self.y1 = self.width, self.height - 1.75*self.incrementY
        self.y1 = self.height - 1.75*self.incrementY # bottom of omniBox

#########################################################################
 

#########################################################################


    def redrawAll(self, canvas):
        self.drawHealthBar(canvas)
        self.drawSleepBar(canvas)
        self.drawMealBlocks(canvas)
        self.drawProductivityBar(canvas)
        self.drawStressBar(canvas)
    
    # draws the health bar
    def drawHealthBar(self, canvas):
        fColor = 'indianRed'
        cr = 10
        x0, y0, x1, y1 = self.width//9, self.y1 + 20, self.width//2 - self.incrementX, self.y1 + 30

        barWidth = x1 - x0
        healthPoints = barWidth / 100 
        dx = char.player.health * healthPoints
        
        
        self.fillThinRoundedRectangle(canvas, x0, y0, x0 + dx, y1, cr, fColor, 0, True)
        self.drawThinRoundedRectangle(canvas, x0, y0, x1, y1, cr, fColor, 'gray', 2, False)

        midY = (y0+y1)//2
        canvas.create_text(x1 + self.incrementX//2, midY, text = f'{round(char.player.health, 1)} / 100', font = 'courier 12 bold', fill = 'gray')

    def drawSleepBar(self, canvas):
        fColor = 'steelBlue1'
        cr = 10
        x0, y0, x1, y1 = self.width//7.5, self.y1 + 60, self.width//2 - self.incrementX, self.y1 + 70
        hourIncrement = (x1 - x0) // 8

        for i in range(8):
            if i != 0:
                canvas.create_line(x0 + i*(hourIncrement), y0, x0 + i*(hourIncrement), y1, fill = 'gray', width = 2)
        
        
        if char.player.sleep > 0:
            self.fillThinRoundedRectangle(canvas, x0, y0, x0 + (char.player.sleep * hourIncrement), y1, cr, fColor, 0, True)
        
        self.drawThinRoundedRectangle(canvas, x0, y0, x1, y1, 10, fColor, 'gray', 2, fill = False)

        midY = (y0+y1)//2
        canvas.create_text(x1 + self.incrementX//2, midY, text = f'{char.player.sleep} / 8', font = 'courier 12 bold', fill = 'gray')

    def drawMealBlocks(self, canvas):
        fColor = 'khaki1'
        cr = 10
        x1, y1 = self.width//6, self.y1 + 110
        x3, y3 = self.width//2 - self.incrementX - (4*cr), y1
        x2, y2 = (x1 + x3)//2, y1

        if char.player.meals == 3:
            canvas.create_oval(x1 - cr, y1 - cr, x1 + cr, y1 + cr, fill = fColor, width = 0)
            canvas.create_oval(x2 - cr, y2 - cr, x2 + cr, y2 + cr, fill = fColor, width = 0)
            canvas.create_oval(x3 - cr, y3 - cr, x3 + cr, y3 + cr, fill = fColor, width = 0)
        elif char.player.meals == 2:
            canvas.create_oval(x1 - cr, y1 - cr, x1 + cr, y1 + cr, fill = fColor, width = 0)
            canvas.create_oval(x2 - cr, y2 - cr, x2 + cr, y2 + cr, fill = fColor, width = 0)
        elif char.player.meals == 1:
            canvas.create_oval(x1 - cr, y1 - cr, x1 + cr, y1 + cr, fill = fColor, width = 0)

        # outlines
        canvas.create_oval(x1 - cr, y1 - cr, x1 + cr, y1 + cr, outline = 'gray', width = 2)
        canvas.create_oval(x2 - cr, y2 - cr, x2 + cr, y2 + cr, outline = 'gray', width = 2)
        canvas.create_oval(x3 - cr, y3 - cr, x3 + cr, y3 + cr, outline = 'gray', width = 2)

        midY = ((y3-cr) + (y3+cr))//2
        x1 = self.width//2 - self.incrementX
        canvas.create_text(x1 + self.incrementX//2, midY, text = f'{char.player.meals} / 3', font = 'courier 12 bold', fill = 'gray')

    def drawProductivityBar(self, canvas):
        fColor = 'springgreen2'
        cr = 10
        xDist = (self.width//2 - self.incrementX) - self.width//9
        x0, y0, x1, y1 = self.width//2 + self.incrementX, self.y1 + 20, self.width//2 + self.incrementX + xDist, self.y1 + 30
        
        barWidth = x1 - x0
        prodPoints = barWidth / 100 
        dx = char.player.productivity * prodPoints
        
        self.fillThinRoundedRectangle(canvas, x0, y0, x0 + dx, y1, cr, fColor, 0, True)
        
        self.drawThinRoundedRectangle(canvas, x0, y0, x1, y1, cr, fColor, 'gray', 2, fill = False)

        midY = (y0+y1)//2
        canvas.create_text(x1 + self.incrementX//2, midY, text = f'{round(char.player.productivity, 1)} / 100', font = 'courier 12 bold', fill = 'gray')
    
    def drawStressBar(self, canvas):
        fColor = 'mediumBlue'
        cr = 10
        xDist = (self.width//2 - self.incrementX) - self.width//9
        indentDist = self.width//7.5 - self.width//9

        x0, y0, x1, y1 = self.width//2 + self.incrementX + indentDist, self.y1 + 80, self.width//2 + self.incrementX + xDist, self.y1 + 90
        
        barWidth = x1 - x0
        stressPoints = barWidth / 100 
        dx = char.player.stress * stressPoints

        self.fillThinRoundedRectangle(canvas, x0, y0, x0 + dx, y1, cr, fColor, 0, True)
        
        self.drawThinRoundedRectangle(canvas, x0, y0, x1, y1, cr, fColor, 'gray', 2, fill = False)

        midY = (y0+y1)//2
        canvas.create_text(x1 + self.incrementX//2, midY, text = f'{round(char.player.stress, 1)} / 100', font = 'courier 12 bold', fill = 'gray')



    # from calendar

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


