import random
import sys
import pygame
from pygame.locals import *


FPS = 32 
SCREENWIDTH = 329
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/bird.png'
BACKGROUND = 'gallery/background.png'
PIPE = 'gallery/pipe.png'

def welcomeScreen():

    playerA = int(SCREENWIDTH/10)
    playerB = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messageA = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messageB = int(SCREENHEIGHT*0.13)
    baseA = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))    
                SCREEN.blit(GAME_SPRITES['player'], (playerA, playerB))    
                SCREEN.blit(GAME_SPRITES['message'], (messageA,messageB ))    
                SCREEN.blit(GAME_SPRITES['base'], (baseA, GROUNDY))    
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score = 0
    playerA = int(SCREENWIDTH/5)
    playerB = int(SCREENWIDTH/2)
    baseA = 0

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # my List of upper pipes
    upperPipes = [
        {'A': SCREENWIDTH+200, 'B':newPipe1[0]['B']},
        {'A': SCREENWIDTH+200+(SCREENWIDTH/2), 'B':newPipe2[0]['B']},
    ]
    # my List of lower pipes
    lowerPipes = [
        {'A': SCREENWIDTH+200, 'B':newPipe1[1]['B']},
        {'A': SCREENWIDTH+200+(SCREENWIDTH/2), 'B':newPipe2[1]['B']},
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8 # velocity while flapping
    playerFlapped = False # It is true only when the bird is flapping


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playerB > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()


        crashTest = isCollide(playerA, playerB, upperPipes, lowerPipes) # This function will return true if the player is crashed
        if crashTest:
            return     

        #check for score
        playerMidPos = playerA + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['A'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
                print(f"Your score is {score}") 
                GAME_SOUNDS['point'].play()


        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False            
        playerHeight = GAME_SPRITES['player'].get_height()
        playerB = playerB + min(playerVelY, GROUNDY - playerB - playerHeight)

        # move pipes to the left
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['A'] += pipeVelX
            lowerPipe['A'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['A']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['A'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['A'], upperPipe['B']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['A'], lowerPipe['B']))

        SCREEN.blit(GAME_SPRITES['base'], (baseA, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerA, playerB))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerA, playerB, upperPipes, lowerPipes):
    if playerB> GROUNDY - 25  or playerB<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playerB < pipeHeight + pipe['B'] and abs(playerA - pipe['A']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playerB + GAME_SPRITES['player'].get_height() > pipe['B']) and abs(playerA - pipe['A']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False

def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()  - 1.2 *offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'A': pipeX, 'B': -y1}, #upper Pipe
        {'A': pipeX, 'B': y2} #lower Pipe
    ]
    return pipe






if __name__ == "__main__":
    # This will be the main point from where our game will start
    pygame.init() # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Sachi Dhaturaha Flappy Bird')
    GAME_SPRITES['numbers'] = ( 
        pygame.image.load('gallery/0.png').convert_alpha(),
        pygame.image.load('gallery/1.png').convert_alpha(),
        pygame.image.load('gallery/2.png').convert_alpha(),
        pygame.image.load('gallery/3.png').convert_alpha(),
        pygame.image.load('gallery/4.png').convert_alpha(),
        pygame.image.load('gallery/5.png').convert_alpha(),
        pygame.image.load('gallery/6.png').convert_alpha(),
        pygame.image.load('gallery/7.png').convert_alpha(),
        pygame.image.load('gallery/8.png').convert_alpha(),
        pygame.image.load('gallery/9.png').convert_alpha(),
    )

    GAME_SPRITES['message'] =pygame.image.load('gallery/message.png').convert_alpha()
    GAME_SPRITES['base'] =pygame.image.load('gallery/base.png').convert_alpha()
    GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180), 
    pygame.image.load(PIPE).convert_alpha()
    )

    # Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen() # Shows welcome screen to the user until he presses a button
        mainGame() # This is the main game function 