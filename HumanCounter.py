import cv2
import mediapipe as mp
import numpy as np
import time
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

basla=time.time()
mp_pose = mp.solutions.pose
ppl=int(0)
dizi=np.array([[]])
a=[]
cap = cv2.VideoCapture("test.mp4")

pose =mp_pose.Pose(
    min_detection_confidence=0.9,
    min_tracking_confidence=0.9) 

while True:
    success, frame = cap.read()
    if not success:
      break

    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]
    aralık1=frameHeight/6*3
    aralık2=frameHeight/6*4
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame)
    if not results.pose_landmarks:
        continue
    for vsbl in results.pose_landmarks.landmark:
        a.append(vsbl.visibility)

    y=int(((results.pose_landmarks.landmark[12].y+results.pose_landmarks.landmark[11].y)/2)*frameHeight)
    x=int(((results.pose_landmarks.landmark[12].x+results.pose_landmarks.landmark[11].x)/2)*frameWidth)
    


    cv2.putText(frame,"Degerlendirme araligi", (5, frameHeight//6*2-10), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 255,255  ), 1, cv2.LINE_AA)
    cv2.line(frame, (0, frameHeight // 6*2), (frameWidth, frameHeight // 6*2), (255, 255, 255), 1)
    cv2.line(frame, (0, frameHeight // 6*4), (frameWidth, frameHeight // 6*4), (255, 255, 255), 1)

    cv2.circle(frame,(x,y),3,(0,255,0),-1)
    cv2.putText(frame, "PPL: " + str(ppl), (20, 30), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 255, 0  ), 1, cv2.LINE_AA)
    frame.flags.writeable = True

    cv2.imshow('Webcam', frame)

    if cv2.waitKey(1) == ord('q'):
        break


y=np.mean(a)
print("dogruluk: "+str(y))
print(ppl)
bitis=time.time()
print("islem suresi: "+ str(bitis-basla))
cap.release()
if cv2.waitKey(1) == ord('q'):
    cv2.destroyAllWindows()
