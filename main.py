import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time

# Load utility images
dividerZone = cv2.imread(f'Resources/Divider.png', cv2.IMREAD_UNCHANGED)
playerScore = cv2.imread(f'Resources/Jugador.png', cv2.IMREAD_UNCHANGED)
aiScore = cv2.imread(f'Resources/AI.png', cv2.IMREAD_UNCHANGED)
 
# Set starting image
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
 
# Detect just one hand
detector = HandDetector(maxHands=1)
 
# Utility variables
timer = 0
resultPause = False
startGame = False
scores = [0, 0]  # [Jugador, IA]
message = ''

def getPlayerMove(hands):
    playerMove = None
    
    hand = hands[0]
    fingers = detector.fingersUp(hand)
    
    if fingers == [0, 0, 0, 0, 0] or fingers == [1, 0, 0, 0, 0]:
        playerMove = 1
    if fingers == [1, 1, 1, 1, 1] or fingers == [0, 1, 1, 1, 1]:
        playerMove = 2
    if fingers == [0, 1, 1, 0, 0]:
        playerMove = 3
            
    return playerMove

def getComputerMove():
    randomNumber = random.randint(1, 3)
    return randomNumber
 
while scores[0] < 5 and scores[1] < 5:
    # Read background image
    imgBG = cv2.imread("Resources/InitialBG.png")
    success, img = cap.read()
    img = cv2.flip(img, 1) # Flipping image so hands are mirrored
    
    # Scale image to fit design
    imgScaled = cv2.resize(img, (0, 0), None, 0.79375, 0.7729)
 
    # Find Hands
    hands, img = detector.findHands(imgScaled, flipType=False)  # Set flipType to false to prevent from swapping each hand
    
     # Put utility images on BG
    imgBG[218:589, 64:572] = imgScaled
    imgBG = cvzone.overlayPNG(imgBG, dividerZone, (500, 355))
    imgBG = cvzone.overlayPNG(imgBG, playerScore, (135, 195))
    imgBG = cvzone.overlayPNG(imgBG, aiScore, (780, 195))
 
    if startGame:
 
        if resultPause is False:
            timer = time.time() - initialTime
            timerText = str(int(timer))
            
            cv2.putText(imgBG, timerText, (610, 435), cv2.FONT_HERSHEY_DUPLEX, 3, (255, 255, 255), 4)
 
            if timer > 3:
                resultPause = True
                timer = 0

                if hands:
                    playerMove = getPlayerMove(hands)
                    computerMove = getComputerMove()
                    
                    imgAI = cv2.imread(f'Resources/{computerMove}.png', cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (860, 320))

                    # Player Wins
                    if (playerMove == 1 and computerMove == 3) or \
                            (playerMove == 2 and computerMove == 1) or \
                            (playerMove == 3 and computerMove == 2):
                        scores[1] += 1
                        message = 'El jugador gana'

                    # AI Wins
                    elif (playerMove == 3 and computerMove == 1) or \
                            (playerMove == 1 and computerMove == 2) or \
                            (playerMove == 2 and computerMove == 3):
                        scores[0] += 1
                        message = 'La IA gana'
                        
                    # Draw
                    elif playerMove == computerMove:
                        message = 'Empate'
                        
                    else:
                        message = 'Error: use una jugada correcta'
                else:
                    message = 'Error: mano no detectada'
 
    if resultPause:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (860, 320))
 
    
    cv2.putText(imgBG, str(scores[0]), (1080, 228), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
    cv2.putText(imgBG, str(scores[1]), (435, 228), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
    cv2.putText(imgBG, message, (520, 680), cv2.FONT_HERSHEY_DUPLEX, 1, (59, 60, 205), 2)
 
    cv2.imshow("BG", imgBG)
 
    key = cv2.waitKey(1)
    if key == ord('x'):
        startGame = True
        initialTime = time.time()
        resultPause = False