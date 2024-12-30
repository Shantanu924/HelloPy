import random, sys, time, pygame
from pygame.locals import *
from pygame import *

pygame.init()

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FLASHSPEED = 500  # in milliseconds
FLASHDELAY = 200  # in milliseconds
BUTTONSIZE = 200
BUTTONGAPSIZE = 20
TIMEOUT = 4  # seconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BRIGHTRED = (255, 0, 0)
RED = (155, 0, 0)
BRIGHTGREEN = (0, 255, 0)
GREEN = (0, 155, 0)
BRIGHTBLUE = (0, 0, 255)
BLUE = (0, 0, 155)
BRIGHTYELLOW = (255, 255, 0)
YELLOW = (155, 155, 0)
DARKGRAY = (40, 40, 40)
bgColor = BLACK

XMARGIN = int((WINDOWWIDTH - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)

# Rectangles for the buttons
YELLOWRECT = pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
BLUERECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN, BUTTONSIZE, BUTTONSIZE)
REDRECT = pygame.Rect(XMARGIN, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
GREENRECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BEEP1, BEEP2, BEEP3, BEEP4

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Simulate')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 16)
    infoSurf = BASICFONT.render('Match the pattern by clicking buttons or using Q, W, A, S keys.', 1, DARKGRAY)
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (10, WINDOWHEIGHT - 25)

    # Load sounds (placeholder if files are missing)
    try:
        BEEP1 = pygame.mixer.Sound('beep1.mp3')
        BEEP2 = pygame.mixer.Sound('beep2.mp3')
        BEEP3 = pygame.mixer.Sound('beep3.mp3')
        BEEP4 = pygame.mixer.Sound('beep4.mp3')
    except pygame.error:
        BEEP1 = BEEP2 = BEEP3 = BEEP4 = None

    pattern = []
    currentStep = 0
    lastClickTime = 0
    score = 0

    waitingForInput = False
    while True:
        clickedButton = None
        DISPLAYSURF.fill(bgColor)
        drawButtons()

        # Display score
        scoreSurf = BASICFONT.render('Score: ' + str(score), 1, WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOWWIDTH - 100, 10)
        DISPLAYSURF.blit(scoreSurf, scoreRect)
        DISPLAYSURF.blit(infoSurf, infoRect)

        checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                clickedButton = getButtonClicked(mousex, mousey)
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    clickedButton = YELLOW
                elif event.key == K_w:
                    clickedButton = BLUE
                elif event.key == K_a:
                    clickedButton = RED
                elif event.key == K_s:
                    clickedButton = GREEN

        if not waitingForInput:
            pygame.display.update()
            pygame.time.wait(1000)
            pattern.append(random.choice((YELLOW, BLUE, RED, GREEN)))
            for button in pattern:
                flashButtonAnimation(button)
                pygame.time.wait(FLASHDELAY)
            waitingForInput = True
        else:
            if clickedButton and clickedButton == pattern[currentStep]:
                flashButtonAnimation(clickedButton)
                currentStep += 1
                lastClickTime = pygame.time.get_ticks()

                if currentStep == len(pattern):
                    changeBackgroundAnimation()
                    score += 1
                    waitingForInput = False
                    currentStep = 0
            elif (clickedButton and clickedButton != pattern[currentStep]) or (currentStep != 0 and pygame.time.get_ticks() - TIMEOUT > lastClickTime):
                gameOverAnimation()
                pattern = []
                currentStep = 0
                waitingForInput = False
                score = 0
                pygame.time.wait(1000)
                changeBackgroundAnimation()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def getButtonRect(color):
    if color == 'YELLOW': return YELLOWRECT
    elif color == 'GREEN': return GREENRECT
    elif color == 'RED': return REDRECT
    elif color == 'BLUE': return BLUERECT 
    return None
def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)


def flashButtonAnimation(color):
    if color == YELLOW:
        flashColor = BRIGHTYELLOW
        sound = BEEP1
        rect = YELLOWRECT
    elif color == BLUE:
        flashColor = BRIGHTBLUE
        sound = BEEP2
        rect = BLUERECT
    elif color == RED:
        flashColor = BRIGHTRED
        sound = BEEP3
        rect = REDRECT
    elif color == GREEN:
        flashColor = BRIGHTGREEN
        sound = BEEP4
        rect = GREENRECT

    if sound:
        sound.play()
    pygame.draw.rect(DISPLAYSURF, flashColor, rect)
    pygame.display.update()
    pygame.time.wait(FLASHSPEED)
    pygame.draw.rect(DISPLAYSURF, color, rect)
    pygame.display.update()


def changeBackgroundAnimation():
    for i in range(3):
        DISPLAYSURF.fill(BRIGHTRED)
        pygame.display.update()
        pygame.time.wait(100)
        DISPLAYSURF.fill(bgColor)
        pygame.display.update()
        pygame.time.wait(100)


def gameOverAnimation():
    for i in range(3):
        DISPLAYSURF.fill(RED)
        pygame.display.update()
        pygame.time.wait(500)
        DISPLAYSURF.fill(bgColor)
        pygame.display.update()
        pygame.time.wait(500)


def getButtonClicked(x, y):
    if YELLOWRECT.collidepoint(x, y):
        return YELLOW
    elif BLUERECT.collidepoint(x, y):
        return BLUE
    elif REDRECT.collidepoint(x, y):
        return RED
    elif GREENRECT.collidepoint(x, y):
        return GREEN
    return None


def drawButtons():
    pygame.draw.rect(DISPLAYSURF, YELLOW, YELLOWRECT)
    pygame.draw.rect(DISPLAYSURF, BLUE, BLUERECT)
    pygame.draw.rect(DISPLAYSURF, RED, REDRECT)
    pygame.draw.rect(DISPLAYSURF, GREEN, GREENRECT)


if __name__ == '__main__':
    main()
