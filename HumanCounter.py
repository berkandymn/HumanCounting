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
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame)
    if not results.pose_landmarks:
        continue
    for vsbl in results.pose_landmarks.landmark:
        a.append(vsbl.visibility)



    mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
    mp_drawing.DrawingSpec(color=(20,250,20), thickness=2, circle_radius=2),
    mp_drawing.DrawingSpec(color=(20,20,250), thickness=2, circle_radius=2))

    cv2.imshow('Webcam', frame)

    bitis=time.time()
    key = cv2.waitKey(1)
    if key == ord('q'):
        break


y=np.mean(a)
print("dogruluk: "+str(y))
print(ppl)
print("islem suresi: "+ str(bitis-basla))
cap.release()
if key == ord('q'):
    cv2.destroyAllWindows()
