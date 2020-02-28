import pygame
from math import pi
from random import randint, sample
from classes import *
from account_management import *

pygame.init()
pygame.font.init()
        
def mainScreen():
    """initilize main screen"""


    clock = pygame.time.Clock()
    window = pygame.display.set_mode((800,600))
    pygame.display.set_caption("Battleship")
    background = pygame.image.load('resources/background.png').convert()
    background = pygame.transform.smoothscale(background, (800,600))
    window.blit(background, (0,0))

    headingFont = pygame.font.Font("resources/PixelFJVerdana12pt.ttf", 40)
    textBattleship = headingFont.render("Battleship", True, (255,255,255))
    window.blit(textBattleship, (224, 50))

    #initialsing buttons
    logInButton = Button(window, (165,510), "Log In", (255,255,255), (25,25,25))
    createAccountButton = Button(window, (465, 510), "Create Account", (255,255,255), (25,25,25))
    
    logInButton.draw()
    createAccountButton.draw()
    
    pygame.display.update()
    
    run = True
    while run:
        clock.tick(60)
        pygame.event.post(pygame.event.Event(1)) #to ensure that the for loop to constantly run
        pygame.display.update()
        
        for event in pygame.event.get():
            if logInButton.action:
                logInButton.action = False
                return logInScreen
            elif createAccountButton.action:
                createAccountButton.action = False
                return createAccountScreen
            
            if event.type == pygame.QUIT:
                #when user exits window from top corner button
                run = False
                pygame.quit()
                break
            
            logInButton.eventHandler(event)
            createAccountButton.eventHandler(event)
    return False


def createAccountScreen():
    """initilize account screen"""
    
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((800,600))
    pygame.display.set_caption("Battleship")
    
    window.fill((50,50,50))
    textFont = pygame.font.Font("resources/PixelFJVerdana12pt.ttf", 15)
    text2Font = pygame.font.Font("resources/PixelFJVerdana12pt.ttf", 10)

    #initialising text field and buttons
    usernameField = TextField(window, (275, 25), "Username:", 500)
    passwordField = TextField(window, (275, 100), "Password:", 500)
    dobField = TextField(window, (275, 175), "Date of Birth:", 500)
    createAccountButton = Button(window, (400,250), "Create Account", (255,255,255), (0,100,200))
    backButton = Button(window, (200,250), "Back", (255,255,255), (0,100,200))
    reqText1 = text2Font.render("Password must fulfill the following:", True, (255,255,255))
    reqText2 = text2Font.render("1.  More than 8 characters", True, (255,255,255))
    reqText3 = text2Font.render("2. At least 1 upper case and lower case", True, (255,255,255))
    reqText4 = text2Font.render("3. At least 1 digit and symbol", True, (255,255,255))
    reqText5 = text2Font.render("4. Cannot contain username", True, (255,255,255))
    
    usernameField.draw()
    passwordField.draw()
    dobField.draw()
    createAccountButton.draw()
    backButton.draw()
    window.blits(((reqText1, (50,325)), (reqText2, (50,350)), (reqText3, (50,375)), (reqText4, (50,400)), (reqText5, (50,425))))

    pygame.display.update()

    timer = 0
    run = True
    while run:  
        clock.tick(60)
        pygame.event.post(pygame.event.Event(1)) #to ensure that the for loop to constantly run
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break
                
            backButton.eventHandler(event)
            createAccountButton.eventHandler(event)
            usernameField.eventHandler(event)
            passwordField.eventHandler(event)
            dobField.eventHandler(event)

            if backButton.action:
                backButton.action = False
                return mainScreen
            elif createAccountButton.action:
                createAccountButton.action = False
                passwordCheckerResults = password_checker(passwordField.text, usernameField.text)
                dobCheckerResults = date_of_birth_checker(dobField.text)
                if not passwordCheckerResults[0]: #when password check fails
                    resultText = textFont.render(passwordCheckerResults[1], True, (200,50,50))
                    if passwordCheckerResults[1] == "Username cannot be empty.":
                        usernameField.drawError()
                    else:
                        passwordField.drawError()
                    pygame.display.update()
                elif not dobCheckerResults[0]: #when dob check fails
                    resultText = textFont.render(dobCheckerResults[1], True, (200,50,50))
                    dobField.drawError()
                else: #when both passes
                    if not store_account(usernameField.text, passwordField.text, dobField.text): #if fail to store account
                        usernameField.drawError()
                        resultText = textFont.render("User already exists.", True, (200,50,50))
                    else:
                        resultText = textFont.render(dobCheckerResults[1], True, (50,200,50)) #return "account created"
                        
                pygame.draw.rect(window, (50,50,50), (150,500,500,100)) #resets the area that the result text takes to background colour
                window.blit(resultText, (150, 500)) #draws the results text onto window

            #tab button handling
            if usernameField.state == 'tab':
                passwordField.active = True
                usernameField.state = None
            elif passwordField.state == 'tab':
                dobField.active = True
                passwordField.state = None
            elif dobField.state == 'tab':
                usernameField.active = True
                dobField.state = None

            #to give the blinking vertical bar on the active text field
            for field in [usernameField, passwordField, dobField]:
                if field.state == 'enter':
                    createAccountButton.action = True
                    field.state = None
                if field.active:
                    if timer % 60 in range(0,31):
                        toPrint = field.text + "|"
                    else:
                        toPrint = field.text
                    field.textShape = field.textFont.render(toPrint, True, (0,0,0))
                    field.drawTriggered()
                    timer+=1 #timer is to allow text box to appear active
    return False

def reactivateAccountScreen():
    """initilize account screen"""

    clock = pygame.time.Clock()
    window = pygame.display.set_mode((800,600))
    pygame.display.set_caption("Battleship")
    
    window.fill((50,50,50))
    textFont = pygame.font.Font("resources/PixelFJVerdana12pt.ttf", 15)

    #initialising text field and buttons
    usernameField = TextField(window, (275,75), "Username:", 500)
    dobField = TextField(window, (275, 150), "Date of Birth:", 500)
    backButton = Button(window, (200,250), "Back", (255,255, 255), (0,100,200))
    reactivateAccountButton = Button(window, (400, 250), "Re-activate account", (255,255,255), (0,100,200)) 
    
    usernameField.draw()
    dobField.draw()
    backButton.draw()
    reactivateAccountButton.draw()
    
    pygame.display.update()

    timer = 0
    run = True
    while run:  
        clock.tick(60)
        pygame.event.post(pygame.event.Event(1)) #to ensure that the for loop to constantly run
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break
                
            backButton.eventHandler(event)
            reactivateAccountButton.eventHandler(event)
            usernameField.eventHandler(event)
            dobField.eventHandler(event)

            if backButton.action:
                backButton.action = False
                return logInScreen
            elif reactivateAccountButton.action:
                reactivateAccountButton.action = False
                result = reactivate_account(usernameField.text, dobField.text)
                if result[0]:
                    resultText = textFont.render(result[1], True, (50,200,50))
                else:
                    if result[1] == "Username not found":
                        usernameField.drawError()
                    elif result[1] == "Incorrect date of birth":
                        dobField.drawError()
                    resultText = textFont.render(result[1], True, (200,50,50))
                    
                pygame.draw.rect(window, (50,50,50), (150,400,500,100)) #resets the area that the result text takes to background colour
                window.blit(resultText, (150, 400)) #draws the results onto the window
                pygame.display.update()

            if usernameField.state == 'tab':
                dobField.active = True
                usernameField.state = None
            elif dobField.state == 'tab':
                usernameField.active = True
                dobField.state = None

            #to give the blinking vertical bar on the active text field
            for field in [usernameField, dobField]:
                if field.state == 'enter':
                    reactivateAccountButton.action = True
                    field.state = None
                if field.active:
                    if timer % 60 in range(0,31):
                        toPrint = field.text + "|"
                    else:
                        toPrint = field.text
                    field.textShape = field.textFont.render(toPrint, True, (0,0,0))
                    field.drawTriggered()
                    timer+=1
    return False

def logInScreen():
    """initilize account screen"""

    clock = pygame.time.Clock()
    window = pygame.display.set_mode((800,600))
    pygame.display.set_caption("Battleship")
    
    window.fill((50,50,50))
    textFont = pygame.font.Font("resources/PixelFJVerdana12pt.ttf", 15)

    #initialising textfields and buttons
    usernameField = TextField(window, (275,75), "Username:", 500)
    passwordField = TextField(window, (275, 150), "Password:", 500)
    logInButton = Button(window, (500,250), "Log In", (255,255,255), (0,100,200))
    backButton = Button(window, (250,250), "Back", (255,255, 255), (0,100,200))
    reactivateAccountButton = Button(window, (50, 525), "Re-activate account", (255,255,255), (0,100,200)) 

    #draws objects onto the screen
    usernameField.draw()
    passwordField.draw()
    logInButton.draw()
    backButton.draw()
    reactivateAccountButton.draw()
    
    pygame.display.update()

    timer = 0
    run = True
    while run:  
        clock.tick(60)
        pygame.event.post(pygame.event.Event(1)) #to ensure that the for loop to constantly run
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break
                
            backButton.eventHandler(event)
            logInButton.eventHandler(event)
            reactivateAccountButton.eventHandler(event)
            usernameField.eventHandler(event)
            passwordField.eventHandler(event)

            if backButton.action:
                backButton.action = False
                return mainScreen
            elif logInButton.action:
                logInButton.action = False
                result = log_in(usernameField.text, passwordField.text)
                if result[0]:
                    return gameScreen
                else:
                    if result[1] == "Username not found":
                        usernameField.drawError()
                    elif result[1] == "Incorrect password":
                        passwordField.drawError()
                    elif result[1] == "Account locked":
                        usernameField.drawError()
                        passwordField.drawError()
                    else:
                        usernameField.drawError()
                        passwordField.drawError()
                    resultText = textFont.render(result[1], True, (200,50,50))
                    
                pygame.draw.rect(window, (50,50,50), (150,400,500,50)) #resets the area that the result text takes to background colour
                window.blit(resultText, (150, 400)) #draws result text onto window
                pygame.display.update()
                
            elif reactivateAccountButton.action:
                reactivateAccountButton.action = False
                return reactivateAccountScreen

            #when user presses tab in a text field
            if usernameField.state == 'tab':
                passwordField.active = True
                usernameField.state = None
            elif passwordField.state == 'tab':
                usernameField.active = True
                passwordField.state = None

            #to give the blinking vertical bar on the active text field
            for field in [usernameField, passwordField]:
                if field.state == 'enter':
                    logInButton.action = True
                    field.state = None
                if field.active:
                    if timer % 60 in range(0,31):
                        toPrint = field.text + "|"
                    else:
                        toPrint = field.text
                    field.textShape = field.textFont.render(toPrint, True, (0,0,0))
                    field.drawTriggered()
                    timer+=1
    return False

def gameScreen():
    """initialise game screen"""
    
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((1280,720))
    pygame.display.set_caption("Battleship")
    background = pygame.image.load("resources/waves.png").convert()
    textFont = pygame.font.Font("resources/PixelFJVerdana12pt.ttf", 15)

    soundTrack = pygame.mixer.music.load("Sea_Ritual.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)

    cellSize = 50

    #initialising buttons, boards, and pieces
    acceptButton = Button(window, (1000,600), "Accept", (255,255,255), (25,25,25))
    nextTurnButton = Button(window, (1000,600), "Next turn", (255,255,255), (25,25,25))
    playAgainButton = Button(window, (700,600), "Play Again", (255,255,255), (25,25,25))
    quitGameButton = Button(window, (1000,600), "Quit Game", (255,255,255), (25,25,25))

    playerBoards = Boards(window, (75,75), cellSize)
    computerBoards = Boards(window, (75,75), cellSize)

    ship = Piece(window, "Ship", cellSize, (1150,300))
    submarine = Piece(window, "Submarine", cellSize, (1150,100))
    comShip = Piece(window, "Ship", cellSize)
    comSubmarine = Piece(window, "Submarine", cellSize)

    #preparing computer's pieces and possible moves
    possibleMoves = [ [z, x, y] for z in range(0,2) for x in range(1,9) for y in range(1,9) ]
    settingUp = True
    while settingUp == True:
        for piece in [comShip, comSubmarine]:
            newOrientation = sample(["H", "V"],1)[0]
            if newOrientation == piece.orientation:
                pass
            else:
                piece.flipOrientation()

        #setting the x y coordinates of ships and submarines
        if comShip.orientation == "H":    
            comShip.coordinates[1:] = [randint(0,9), randint(2,8)]
        else:
            comShip.coordinates[1:] = [randint(1,7), randint(0,9)]

        if comSubmarine.orientation == "H":
            comSubmarine.coordinates[1:] = [randint(0,9), randint(1,8)]
        else:
            comSubmarine.coordinates[1:] = [randint(1,8), randint(0,9)]
        comShip.coordinates[0] = 0
        comSubmarine.coordinates[0] = sample([0,0,0,1,1,1,1],1)[0] #submarine has 2x chance to be in subsea

        #if there was overlap, reset and try again
        for piece in [comShip, comSubmarine]:
            computerBoards.placePiece(piece)
        if computerBoards.checkNumShipSub() == (4,3):
            settingUp = False
        else:
            computerBoards.reset()

    #initializing other variables
    playingGame = False
    playerTurn, computerTurn, turnOver = True, False, False
    x = 0
    firstLineTest = "Please place the ship and submarine. Once done, click \"accept\"!"
    secondLineText = "Right click while placing to rotate!"
    errorText = ""

    timer = 0
    run = True
    while run:
        clock.tick(60)
        pygame.event.post(pygame.event.Event(1)) #to ensure that the for loop to constantly run
        pygame.display.update()
        
        for event in pygame.event.get():

            #moving the background image across the screen
            x -= 0.1
            relative_x = x % background.get_rect().width
            window.blit(background, (relative_x - background.get_rect().width, 0))
            if relative_x < 1280:
                window.blit(background, (relative_x, 0))
            
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break

            textSurface = textFont.render(firstLineTest, True, (255,255,255))
            piecesLeftSurface = textFont.render(secondLineText, True, (255,255,255))
            window.blit(textSurface, (20, 600))
            window.blit(piecesLeftSurface, (20, 640))
            
            #prep phase where pieces are being placed
            if not playingGame:

                #event handlers also bilts the objects onto the screen
                ship.eventHandler(event)
                submarine.eventHandler(event)
                acceptButton.eventHandler(event)
                
                playerBoards.update()
                
                errorTextSurface = textFont.render(errorText, True, (200,50,50))
                window.blit(errorTextSurface, (500, 640))
                
                if ship.active:
                    ship.surfaceBackground = window.copy()
                    ship.trace()
                    submarine.draw()
                elif submarine.active:
                    submarine.surfaceBackground = window.copy()
                    submarine.trace()
                    ship.draw()
                else:
                    ship.draw()
                    submarine.draw()
                
                if acceptButton.action:
                    if ship.placed and submarine.placed:
                        for piece in [ship, submarine]:
                            playerBoards.placePiece(piece)
                        if playerBoards.checkNumShipSub() == (4,3):
                            playingGame = True
                            playerBoards.playing = True
                            acceptButton.action = False
                            secondLineText = ""
                        else:
                            playerBoards.reset()
                            errorText = "No overlapping!"
                            acceptButton.action = False
                    else:
                        errorText = "Please place the pieces!"
                        acceptButton.action = False

            #game phase starts
            elif playingGame:
                
                #computer's turn
                if computerTurn:
                    ship.draw()
                    submarine.draw()
                    playerBoards.update()
                    if playerBoards.checkNumShipSub() == (0,0):
                        #game over condition
                        firstLineTest = "YOU LOSE!"
                        secondLineText = ""
                        playAgainButton.eventHandler(event)
                        quitGameButton.eventHandler(event)
                        if playAgainButton.action:
                            return gameScreen
                        elif quitGameButton.action:
                            pygame.quit()
                            run = False
                            break
                    else:
                        #computer selecting coordinate
                        secondLineText = "You have {0[0]}/4 ship and {0[1]}/3 submarine left.".format(playerBoards.checkNumShipSub())
                        if timer < 60 and not turnOver:
                            #artifical delay to appear as if the computer is thinking
                            firstLineTest = "Computer's Turn."
                            timer += 1
                        elif not turnOver:
                            nextTurnButton.action = False
                            coordinates = sample(possibleMoves,1)[0]
                            possibleMoves.remove(coordinates)
                            playerBoards.receiveAttack(coordinates)
                            if playerBoards.validMove:
                                playerBoards.validMove = False
                                turnOver = True
                            
                        else:
                            nextTurnButton.eventHandler(event)
                            firstLineTest = "Computer's Turn is over. Press next when you're ready!"
                            if turnOver:
                                if nextTurnButton.action:
                                    timer = 0
                                    computerTurn = False
                                    playerTurn = True
                                    turnOver = False
                                    nextTurnButton.action = False
                                    
                #player's turn
                elif playerTurn:
                    computerBoards.update()
                    if computerBoards.checkNumShipSub() == (0,0):
                        #game over condition
                        firstLineTest = "YOU WIN!"
                        secondLineText = ""
                        playAgainButton.eventHandler(event)
                        quitGameButton.eventHandler(event)
                        if playAgainButton.action:
                            return gameScreen
                        elif quitGameButton.action:
                            pygame.quit()
                            run = False
                            break
                    else:
                        #player selecting coordinate
                        secondLineText = "Enemy has {0[0]}/4 ship and {0[1]}/3 submarine left.".format(computerBoards.checkNumShipSub())
                        if not turnOver:
                            firstLineTest = "Your turn."
                            computerBoards.eventHandler(event)
                            if computerBoards.validMove:
                                #if user made a valid move then go to next turn
                                computerBoards.validMove = False
                                turnOver = True
                        else:
                            firstLineTest = "Your Turn is over. Press next when you're ready!"
                            nextTurnButton.eventHandler(event)
                            if nextTurnButton.action:
                                computerTurn = True
                                playerTurn = False
                                turnOver = False
                                nextTurnButton.action = False
                            
            #piece placement section           
            if ship.placePiece:
                if playerBoards.checkIfCollide(event.pos):
                    for boardIndex, board in enumerate(playerBoards.boards):
                        for rowIndex, row in enumerate(board):
                            for colIndex, element in enumerate(row):
                                if element.checkIfCollide(event.pos):
                                    ship.place(element.rect)
                                    ship.coordinates = (boardIndex, rowIndex, colIndex)
                                    if boardIndex == 1:
                                        errorText = "Ship cannot be underwater!"
                                    elif ship.orientation == "H" and colIndex not in range(2,9):
                                        errorText = "Ship is out of range!"
                                    elif ship.orientation == "V" and rowIndex not in range(1,8):
                                        errorText = "Ship is out of range!"
                                    else:
                                        ship.placed = True
                ship.placePiece = False
            if submarine.placePiece:
                if playerBoards.checkIfCollide(event.pos):
                    for boardIndex, board in enumerate(playerBoards.boards):
                        for rowIndex, row in enumerate(board):
                            for colIndex, element in enumerate(row):
                                if element.checkIfCollide(event.pos):
                                    submarine.place(element.rect)
                                    submarine.coordinates = [boardIndex, rowIndex, colIndex]
                                    if submarine.orientation == "H" and colIndex not in range(1,9):
                                        errorText = "Submarine out of range!"
                                    elif submarine.orientation == "V" and rowIndex not in range(1,9):
                                        errorText = "Submarine out of range!"
                                    else:
                                        submarine.placed = True
                submarine.placePiece = False
    return False

current = mainScreen()                    
while True:
    if current == False:
        break
    current = current()
