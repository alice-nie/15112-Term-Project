from cmu_112_graphics import *

class Alice(App):
    
    def appStarted(self):

        playerSpriteSheet = self.loadImage('playerSpriteSheet.png')
        self.resizedPlayerSpriteSheet = self.scaleImage(playerSpriteSheet, 3/4) 
        playerSheetWidth, playerSheetHeight = self.resizedPlayerSpriteSheet.size
        self.incrementX = playerSheetWidth / 9
        self.incrementY = playerSheetHeight / 4
        incrementX, incrementY = self.incrementX, self.incrementY

        self.barBoxTop = self.height - (self.incrementY//2)- 10


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


    def keyPressed(self, event):
        if event.key == 'w' or event.key == 'a' or event.key == 's' or event.key == 'd':
            
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

    def playerMoveIsLegal(self):
        x, y = self.playerLocation
        portionOfSpriteWidth = self.incrementX * (2/5)
        portionOfSpriteHeight = self.incrementY * (2/5)
        if ((0 + portionOfSpriteWidth <= x < self.width - portionOfSpriteWidth) and
            (0 + portionOfSpriteHeight <= y < self.barBoxTop - portionOfSpriteHeight)):
            return True
        return False

    def redrawAll(self, canvas):
        x, y = self.playerLocation
        sprite = self.currentPlayerSprite
        canvas.create_image(x, y, image = ImageTk.PhotoImage(sprite))


Alice(width=1440, height = 778)