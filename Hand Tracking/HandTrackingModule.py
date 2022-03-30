import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands #there are total three (2folder and 1 file) and the heiarchy is a folder mp inside there is a folder inside that there is a file called hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils#there are total two (1folder & file) and the heiarchy is a folder mp inside there is a solutions file inside that there is a function named as drawing_utils
    
    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB) # process function which is inside hands object is called and perform some action(medial solution result) and store in self.result
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks: #if two habds are there than one by one hands will be iterated 
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img
    
    def findPosition(self, img, handNo=0, draw=True): 
        lmList = []
        if self.results.multi_hand_landmarks:
            "Hello world"
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)


        return lmList
def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    detector = handDetector()

    while True:
        
        success, img = cap.read()
        
        img = detector.findHands(img)
        lmlist = detector.findPosition(img)
        if len(lmlist)!=0:
            print(lmlist[4])    
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
            
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                        (255, 0, 255), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)



if __name__ == "__main__":
    main()



# by going inside of that particular file there is a class with name Hands so basically self.hands is a object of Hands class

