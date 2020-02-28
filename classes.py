import pygame
from math import pi
from math import sqrt
from string import punctuation, digits, ascii_letters

class Button:
    """object contains Font blited onto a Rect"""

    def __init__(self, surface, location, text, textColour, buttonColour, textSize=15):
        """Surface, (int,int), string, int, (int,int,int), (int,int,int)) -> Button"""

        textFont = pygame.font.Font("resources/PixelFJVerdana12pt.ttf", textSize)
        
        self.surface = surface
        self.location = location
        self.textColour = textColour
        self.buttonColour = buttonColour
        self.buttonTriggeredColour = (buttonColour[0]+25, buttonColour[1]+25, buttonColour[2]+25)
        self.textSurface = textFont.render(text, True, self.textColour)

        self.size = self.textSurface.get_size()
        self.rect = pygame.Rect(self.location, (self.size[0]+10, self.size[1]+15))
        self.rightSemi = self.generateRightSemi(self.rect.topright)
        self.leftSemi = self.generateLeftSemi(self.rect.topleft)

        #intialising state attributes
        self.active = False
        self.action = False
        self.collide = False

    def eventHandler(self, event):
        """event handler for button, sets action state to true when user successfully clicks button"""
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.checkIfCollide(event.pos):
            self.drawTriggered()
            self.active = True
            self.collide = True
        elif self.active == True:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                #when user lets go of left click while on the button
                if self.collide:
                    self.draw()
                    self.active = False
                    self.action = True
                else:
                    self.draw()
                    self.active = False
            elif event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
                #when user moves mouse while holding down left click
                if self.checkIfCollide(event.pos):
                    self.collide = True
                    self.drawTriggered()
                else:
                    self.collide = False
                    self.draw()
            elif self.collide:
                self.drawTriggered()
            else:
                self.draw()
        else:
            self.draw()
                    
    def determine_y(self, radius, x):
        """equation used to draw semicircles"""
        
        return (sqrt(radius**2 - x**2))
    
    def generateRightSemi(self, topRight):
        """takes in coordinate of top right of main rect and returns a list of rects that represent the right semi circle of the button"""

        list_rects = []
        x = 1
        y = self.rect.height
        z = (self.rect.height-y)/2
        while x<=self.rect.height/2:
            list_rects.append(pygame.Rect((topRight[0], topRight[1]+z), (x,y)))
            y = self.determine_y(self.rect.height/2, x)*2
            x += 1
            z = (self.rect.height-y)/2
        return list_rects

    def generateLeftSemi(self, topLeft):
        """takes in coordinate of top left of main rect and returns a list of rects that represent the left semi circle of the button"""

        list_rects = []
        x = 1
        y = self.rect.height/2
        z = (self.rect.height-y)/2
        while x<=self.rect.height/2:
            list_rects.append(pygame.Rect((topLeft[0]-x, topLeft[1]+z), (x,y)))
            y = self.determine_y(self.rect.height/2, x)*2
            x += 1
            z = (self.rect.height-y)/2
        return list_rects
                              
    def draw(self):
        """bilts Button object onto window"""
        
        pygame.draw.rect(self.surface, self.buttonColour, self.rect)
        self.surface.blit(self.textSurface, self.rect, (-7,-8, self.size[0]+10, self.size[1]+15))
        for rect in self.rightSemi:
            pygame.draw.rect(self.surface, self.buttonColour, rect)
        for rect in self.leftSemi:
            pygame.draw.rect(self.surface, self.buttonColour, rect)

    def drawTriggered(self):
        """bilts Button object triggered onto window"""

        pygame.draw.rect(self.surface, self.buttonTriggeredColour, self.rect)
        self.surface.blit(self.textSurface, self.rect, (-7,-8, self.size[0]+10, self.size[1]+15))
        for rect in self.rightSemi:
            pygame.draw.rect(self.surface, self.buttonTriggeredColour, rect)
        for rect in self.leftSemi:
            pygame.draw.rect(self.surface, self.buttonTriggeredColour, rect)

    def checkIfCollide(self, mousePos):
        """returns if Button collides with event position"""
        
        for rect in self.leftSemi:
            if rect.collidepoint(mousePos):
                return True
        for rect in self.rightSemi:
            if rect.collidepoint(mousePos):
                return True
        if self.rect.collidepoint(mousePos):
            return True
        else:
            return False
                

class TextField:
    """object contains a Header Text bilted on the left of a working text field"""

    def __init__(self, surface, location, headerText , length, textSize=15):
        """(Surface, (int, int), string,  int, int) -> TextField"""

        self.textFont = pygame.font.Font("resources/PixelFJVerdana12pt.ttf", textSize)

        self.headerSurface = self.textFont.render(headerText, True, (255,255,255)) #Surface for text before the text field
        
        self.surface = surface
        self.location = location
        self.height = self.textFont.size("Hello World")[1] #sample text to get height of text field
        self.length = length
        self.rect = pygame.Rect(location, (self.length, self.height+20)) #rect representing text field
        self.text = ""
        self.active = False
        self.state = None
        self.validKeys = digits + ascii_letters + punctuation
        self.surface.blit(self.headerSurface, (self.location[0] - 250, self.location[1] + 10))
        

    def eventHandler(self, event):
        """event handler for text field"""
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.checkIfCollide(event.pos):
                self.drawTriggered()
                self.active = True
                self.state = None
            else:
                self.draw()
                self.active = False
                self.state = None

        if event.type == pygame.KEYDOWN and self.active:
            self.state = None
            if event.unicode in self.validKeys:
                if len(self.text) >= 16:
                    pass
                else:
                    self.text += event.unicode
            elif event.key == 8: 
                self.text = self.text[:-1]
            elif event.key == 27 :
                self.active = False
                self.draw()
                self.state = "esc"
            elif event.key == 9:
                self.active = False
                self.draw()
                self.state = "tab"
            elif event.key == 13:
                self.active = False
                self.draw()
                self.state = "enter"
            
    def draw(self):
        """draws the text field and text onto window"""
        
        self.surface.fill((255,255,255), self.rect)
        pygame.draw.rect(self.surface, (10,10,10), self.rect, 2)
        self.textShape = self.textFont.render(self.text, True, (0,0,0))
        self.surface.blit(self.textShape, self.rect, (-5, -10, self.location[0]+295, self.location[1]+20))

    def drawTriggered(self):
        """draws the triggered text field and text onto window"""
        
        self.surface.fill((255,255,255), self.rect)
        pygame.draw.rect(self.surface, (0,0,200), self.rect, 2)
        self.surface.blit(self.textShape, self.rect, (-5, -10, self.location[0]+295, self.location[1]+20))

    def drawError(self):
        """blits the error text field onto window"""
        
        self.surface.fill((255,255,255), self.rect)
        pygame.draw.rect(self.surface, (200,50,50), self.rect, 2)
        self.surface.blit(self.textShape, self.rect, (-5, -10, self.location[0]+295, self.location[1]+20))

    def checkIfCollide(self, mousePos):
        """returns Boolean whether mouse left clicks on text field"""
        
        if self.rect.collidepoint(mousePos):
            return True
        else:
            return False



class Boards:
    """object containing a list of 2 individual boards, which each consists of 10x10 cells"""
    
    class Cell:
        """object represents individual cell in board"""
        
        def __init__(self, surface, location, size):
            """(surface, (int,int), int) -> Cell"""
            
            self.surface = surface
            self.location = location
            self.size = size

            #initialising variables
            self.rect = pygame.Rect(location, (self.size,self.size))
            self.state = "O" #O for empty, H for hit, M for miss
            self.receivingAttack = False

            #initialising images
            self.crossImg = pygame.image.load("resources/cross.png").convert_alpha()
            self.crossFadedImg = pygame.image.load("resources/crossFaded.png").convert_alpha()
            self.explosionImg = pygame.image.load("resources/explosion.png").convert_alpha()
            self.crossImg = pygame.transform.smoothscale(self.crossImg, (self.size-2,self.size-2))
            self.crossFadedImg = pygame.transform.smoothscale(self.crossFadedImg, (self.size-2,self.size-2))
            self.explosionImg = pygame.transform.smoothscale(self.explosionImg, (self.size-2, self.size-2))

        def __eq__(self, other):
            """equality method"""
            
            if self.state == other:
                return True
            else:
                return False

        def drawBorders(self):
            """draw the borders of cell"""
            
            pygame.draw.rect(self.surface, (0,0,0), self.rect, 1)

        def drawState(self):
            """draws when cell is hit"""
            if self.state == "O":
                pass
            elif self.state == "M":
                self.surface.blit(self.crossImg, self.rect, (-1,-1,self.size-1,self.size-1))
            elif self.state == "H":
                self.surface.blit(self.explosionImg, self.rect, (-1,-1,self.size-1,self.size-1))
            if self.receivingAttack:
                self.surface.blit(self.crossFadedImg, self.rect, (-1,-1,self.size-1,self.size-1))

        def checkIfCollide(self, mousePos):
            """returns if mouse collides with cell"""
            
            rect = pygame.Rect(self.rect.x + 1, self.rect.y + 1, self.rect.w - 2, self.rect.h -2)
            if rect.collidepoint(mousePos):
                return True
            else:
                return False

    def __init__(self, surface, location, size):
        """(Surface, (int,int), int) -> Boards

        """
        self.surface = surface
        self.location = location
        self.size = size

        self.playing = False
        self.boards = []
        self.rect = pygame.Rect(location, (29*(size-1),29*(size-1)))
        self.receivingAttack = False
        self.validMove = False

        #initialising the header text for each board
        textFont = pygame.font.Font("resources/PixelFJVerdana12pt.ttf", 15)
        surfaceText, subseaText = "Surface", "Subsea"
        self.surfaceSurface = textFont.render(surfaceText, True, (0,0,0))
        self.subseaSurface = textFont.render(subseaText, True, (0,0,0))

        #creating the 2 boards with 10x10 cells each
        singleBoard = []
        for row in range(0,10):
            row = [self.Cell(self.surface, (self.location[0]+col*(self.size -1),self.location[1]+row*(self.size-1)), self.size) for col in range(0,10)]
            singleBoard.append(row)
        self.boards.append(singleBoard)
        singleBoard = []
        for row in range(0,10):
            row = [self.Cell(self.surface, (self.location[0]+self.size*11+col*(self.size -1),self.location[1]+row*(self.size-1)), self.size) for col in range(0,10)]
            singleBoard.append(row)
        self.boards.append(singleBoard)

    def eventHandler(self, event):
        """this handles when player is choosing where to attack"""
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.checkIfCollide(event.pos):
            #when player left clicks onto the board
            self.receivingAttack = True
            for boardIndex, board in enumerate(self.boards):
                for rowIndex, row in enumerate(board):
                    for colIndex, element in enumerate(row):
                        if element.checkIfCollide(event.pos):
                            if rowIndex == 0:
                                if colIndex == 0:
                                    for row2 in self.boards[boardIndex][rowIndex:rowIndex+2]:
                                        for ele in row2[colIndex:colIndex+2]:
                                            ele.receivingAttack = True
                                else:
                                    for row2 in self.boards[boardIndex][rowIndex:rowIndex+2]:
                                        for ele in row2[colIndex-1:colIndex+2]:
                                            ele.receivingAttack = True
                            else:
                                if colIndex == 0:
                                    for row2 in self.boards[boardIndex][rowIndex-1:rowIndex+2]:
                                        for ele in row2[colIndex:colIndex+2]:
                                            ele.receivingAttack = True
                                else:
                                    for row2 in self.boards[boardIndex][rowIndex-1:rowIndex+2]:
                                        for ele in row2[colIndex-1:colIndex+2]:
                                            ele.receivingAttack = True
        if self.receivingAttack:
            if event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
                #when player moves mouse while left mouse button is engaged
                self.resetCellReceivingAttackState()
                if self.checkIfCollide(event.pos):
                    for boardIndex, board in enumerate(self.boards):
                        for rowIndex, row in enumerate(board):
                            for colIndex, element in enumerate(row):
                                if element.checkIfCollide(event.pos):
                                    if rowIndex == 0:
                                        if colIndex == 0:
                                            for row2 in self.boards[boardIndex][rowIndex:rowIndex+2]:
                                                for ele in row2[colIndex:colIndex+2]:
                                                    ele.receivingAttack = True
                                        else:
                                            for row2 in self.boards[boardIndex][rowIndex:rowIndex+2]:
                                                for ele in row2[colIndex-1:colIndex+2]:
                                                    ele.receivingAttack = True
                                    else:
                                        if colIndex == 0:
                                            for row2 in self.boards[boardIndex][rowIndex-1:rowIndex+2]:
                                                for ele in row2[colIndex:colIndex+2]:
                                                    ele.receivingAttack = True
                                        else:
                                            for row2 in self.boards[boardIndex][rowIndex-1:rowIndex+2]:
                                                for ele in row2[colIndex-1:colIndex+2]:
                                                    ele.receivingAttack = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                #when player releases left mouse button
                if self.checkIfCollide(event.pos):
                    counter = 0
                    for boardIndex, board in enumerate(self.boards):
                        for rowIndex, row in enumerate(board):
                            for colIndex, element in enumerate(row):
                                if element.receivingAttack:
                                    if element.state == "O":
                                        element.state = "M"
                                        counter += 1
                                    elif element.state == "Ship" or element.state == "Submarine":
                                        element.state = "H"
                                        counter += 1
                    if counter == 0:
                        self.receivingAttack = False
                        self.resetCellReceivingAttackState()
                    else:
                        self.receivingAttack = False
                        self.validMove = True
                        self.resetCellReceivingAttackState()
                else:
                    self.receivingAttack = False

    def receiveAttack(self, coord):
        """changes the states of the cells that receive an attack, for enemies's attack only"""

        self.resetCellReceivingAttackState()
        if coord[1] == 0:
            if coord[2] == 0:
                for row2 in self.boards[coord[0]][coord[1]:coord[1]+2]:
                    for ele in row2[coord[2]:coord[2]+2]:
                        ele.receivingAttack = True
            else:
                for row2 in self.boards[coord[0]][coord[1]:coord[1]+2]:
                    for ele in row2[coord[2]-1:coord[2]+2]:
                        ele.receivingAttack = True
        else:
            if coord[2] == 0:
                for row2 in self.boards[coord[0]][coord[1]-1:coord[1]+2]:
                    for ele in row2[coord[2]:coord[2]+2]:
                        ele.receivingAttack = True
            else:
                for row2 in self.boards[coord[0]][coord[1]-1:coord[1]+2]:
                    for ele in row2[coord[2]-1:coord[2]+2]:
                        ele.receivingAttack = True
        counter = 0
        for boardIndex, board in enumerate(self.boards):
            for rowIndex, row in enumerate(board):
                for colIndex, element in enumerate(row):
                    if element.receivingAttack:
                        if element.state == "O":
                            element.state = "M"
                            counter += 1
                        elif element.state == "Ship" or element.state == "Submarine":
                            element.state = "H"
                            counter += 1
        if counter == 0:
            self.resetCellReceivingAttackState()
        else:
            self.validMove = True
            self.resetCellReceivingAttackState()
                        
    def checkNumShipSub(self):
        """returns number of ships and submarines left in the board"""
        
        counter_ship = 0
        counter_sub = 0
        for board in self.boards:
            for row in board:
                for element in row:
                    if element == 'Ship':
                        counter_ship += 1
                    elif element == 'Submarine':
                        counter_sub += 1
        return (counter_ship, counter_sub)

    def placePiece(self, piece):
        """changes the state of the appropriate cells to a ship or submarine"""
        
        if piece.name == "Ship":
            if piece.orientation == "H":
                for col in range(piece.coordinates[2] - 2, piece.coordinates[2] + 2):
                    self.boards[piece.coordinates[0]][piece.coordinates[1]][col].state = "Ship"
            else:
                for row in range(piece.coordinates[1] - 1, piece.coordinates[1] + 3):
                    self.boards[piece.coordinates[0]][row][piece.coordinates[2]].state = "Ship"
        if piece.name == "Submarine":
            if piece.orientation == "H":
                for col in range(piece.coordinates[2] - 1, piece.coordinates[2] + 2):
                    self.boards[piece.coordinates[0]][piece.coordinates[1]][col].state = "Submarine"
            else:
                for row in range(piece.coordinates[1] - 1, piece.coordinates[1] + 2):
                    self.boards[piece.coordinates[0]][row][piece.coordinates[2]].state = "Submarine"

    def checkIfCollide(self, mousePos):
        """returns if mouse collides with board"""
        
        for board in self.boards:
            for row in board:
                for element in row:
                    if element.checkIfCollide(mousePos):
                        return True
        return False

    def update(self):
        """blits board names and each cell onto screen"""
        
        for board in self.boards:
            for row in board:
                for element in row:
                    element.drawBorders()
                    element.drawState()
        self.surface.blit(self.surfaceSurface, (250,25))
        self.surface.blit(self.subseaSurface, (250 + self.size*11, 25))

    def reset(self):
        """resets the boards to original empty state"""
        
        self.boards = []
        singleBoard = []
        for row in range(0,10):
            row = [self.Cell(self.surface, (self.location[0]+col*(self.size -1),self.location[1]+row*(self.size-1)), self.size) for col in range(0,10)]
            singleBoard.append(row)
        self.boards.append(singleBoard)
        singleBoard = []
        for row in range(0,10):
            row = [self.Cell(self.surface, (self.location[0]+self.size*11+col*(self.size -1),self.location[1]+row*(self.size-1)), self.size) for col in range(0,10)]
            singleBoard.append(row)
        self.boards.append(singleBoard)

    def resetCellReceivingAttackState(self):
        """resets the boards' receiving attack states"""
        
        for boardIndex, board in enumerate(self.boards):
            for rowIndex, row in enumerate(board):
                for colIndex, element in enumerate(row):
                    element.receivingAttack = False

class Piece:
    """object representing the ship or submarine piece"""

    def __init__(self, surface, name, size, location=(0,0)):
        """(surface, string) -> Piece object"""

        self.surface = surface
        self.name = name
        self.location = location
        self.size = size

        self.surfaceBackground = surface.copy()
        self.orientation = "V"
        self.coordinates = [int,int,int]
        self.active = False #state to handle when the piece is picked up
        self.placePiece = False #state to handle when user accepts the piece's position by clicking accept
        self.placed = False #state to handle when user places the piece onto the board
        
        if self.name == "Ship":
            self.image = pygame.image.load("resources/ship.png").convert_alpha()
            self.imageH = pygame.transform.smoothscale(self.image, (self.size*4 -2, self.size-2))
            self.imageV = pygame.transform.rotate(self.imageH, 90)
        elif self.name == "Submarine":
            self.image = pygame.image.load("resources/submarine.png").convert_alpha()
            self.imageH = pygame.transform.smoothscale(self.image, (self.size*3 -2, self.size-2))
            self.imageV = pygame.transform.rotate(self.imageH, 90)
        self.rect = self.imageV.get_rect(topleft=location)

    def eventHandler(self, event):
        """event handler for when user clicks on piece, puts the piece down, and moves the piece"""

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.checkIfCollide(event.pos) and not self.active:
            self.active = True
            self.placePiece = False
            self.placed = False
            #when clicks onto piece
        elif self.active:
            if event.type == pygame.MOUSEMOTION:
                #when piece is moved, change rect location to mouse position
                if self.name == "Ship":
                    if self.orientation == "H":
                        self.rect.center = (event.pos[0] - self.size/2, event.pos[1])
                    else:
                        self.rect.center = (event.pos[0], event.pos[1]+self.size/2)
                else:
                    if self.orientation == "H":
                        self.rect.center = (event.pos[0], event.pos[1])
                    else:
                        self.rect.center = (event.pos[0], event.pos[1])
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                #when right click to rotate piece
                if self.orientation == "H":
                    self.orientation = "V"
                    self.rect.w, self.rect.h = self.rect.h, self.rect.w
                    self.rect.center = (event.pos[0], event.pos[1]+self.size/2)
                else:
                    self.orientation = "H"
                    self.rect.w, self.rect.h = self.rect.h, self.rect.w
                    self.rect.center = (event.pos[0] - self.size/2, event.pos[1])
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                #when piece is dropped
                self.active = False
                self.placePiece = True

    def draw(self):
        """blits the piece onto the surface"""
        
        if self.orientation == "H":
            self.surface.blit(self.imageH, self.rect.topleft)
        else:
            self.surface.blit(self.imageV, self.rect.topleft)

    def trace(self):
        """blits image of the piece onto mouse cursor location based on rect location"""
        
        self.surface.blit(self.surfaceBackground, (0,0))
        if self.orientation == "H":
            self.surface.blit(self.imageH, self.rect.topleft)
        else:
            self.surface.blit(self.imageV, self.rect.topleft)

    def place(self, rect):
        """when user pieces piece onto board"""
        
        self.surface.blit(self.surfaceBackground, (0,0))
        if self.name == "Ship":
            if self.orientation == "H":
                self.surface.blit(self.imageH, rect.topleft, (-1,-1,self.size-1,self.size-1))
                self.rect.center = (rect.center[0] - self.size/2, rect.center[1])
            else:
                self.surface.blit(self.imageV, rect.topleft, (-1,-1,self.size-1,self.size-1))
                self.rect.center = (rect.center[0], rect.center[1]+self.size/2)
        else:
            if self.orientation == "H":
                self.surface.blit(self.imageH, rect.topleft, (-1,-1,self.size-1,self.size-1))
                self.rect.center = (rect.center[0], rect.center[1])
            else:
                self.surface.blit(self.imageV, rect.topleft, (-1,-1,self.size-1,self.size-1))
                self.rect.center = (rect.center[0], rect.center[1])
        self.placePiece = False
        
    def checkIfCollide(self, mousePos):
        """returns if mouse collides with piece"""
        
        if self.rect.collidepoint(mousePos):
            return True
        else:
            return False
        
    def flipOrientation(self):
        """sets piece's orientation"""
        if self.orientation == "V":
            self.orientation = "H"
        else:
            self.orientation = "V"
