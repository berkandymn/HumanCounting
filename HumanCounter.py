import cv2
import numpy as np
import time
import mqttClient as mqtt

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2

basla=time.time()
bitis=time.time()

mp_pose = mp.solutions.pose
ppl=mqtt.ilkDeger()
dizi=np.array([[]])
a=[]

x=np.array([[]])
y=np.array([[]])
hassasiyet=[]
boxes_ids=0

cap = cv2.VideoCapture("test.mp4")

mqttMessage=0

base_options = python.BaseOptions(model_asset_path='pose_landmarker_full.task')
options = vision.PoseLandmarkerOptions(
    base_options=base_options,
    output_segmentation_masks=True,
    min_pose_detection_confidence=0.68,
    min_pose_presence_confidence=0.55,
    min_tracking_confidence=0.6,
    num_poses=5)
detector = vision.PoseLandmarker.create_from_options(options)

while cap.isOpened():
    detections = []
    success, frame = cap.read()
    if not success:
      break
    
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    aralık1=frameHeight/6*3
    aralık2=frameHeight/6*4

    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
    detection_result = detector.detect(mp_image)

    pose_landmarks_list = detection_result.pose_landmarks
    frame = np.copy(mp_image.numpy_view())
    
    for idx in range(len(pose_landmarks_list)):
        pose_landmarks = pose_landmarks_list[idx]

        #kişinin vücut noktaları ataması yapılıyor
        pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        pose_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z,visibility=landmark.visibility) for landmark in pose_landmarks
        ])

        #kendi belirlediğimiz üst vücut merkez noktası için x-y koordinat ataması yapılıyor. Ayırt etmek için bir nokta çiziliyor.
        y = int(((pose_landmarks_proto.landmark[12].y + pose_landmarks_proto.landmark[11].y) / 2) * frameHeight)
        x = int(((pose_landmarks_proto.landmark[12].x + pose_landmarks_proto.landmark[11].x) / 2) * frameWidth)
        cv2.circle(frame, (x, y), 3, (0, 0, 255), -1)
        #algılama hassasiyeti bir diziye atanıyor
        hassasiyet.append(pose_landmarks_proto.landmark[12].visibility)

        #kişi belirlenen aralığa girdiğinde takip ve hesaplama modeline konum bilgisi gönderiliyor
        if aralık1-20 < y < aralık2+20:
            detections.append([x, y])

    cv2.putText(frame,"Degerlendirme araligi", (5, frameHeight//6*2-10), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 255,255  ), 1, cv2.LINE_AA)
    cv2.line(frame, (0, frameHeight // 6*2), (frameWidth, frameHeight // 6*2), (255, 255, 255), 1)
    cv2.line(frame, (0, frameHeight // 6*4), (frameWidth, frameHeight // 6*4), (255, 255, 255), 1)
    

    #Algılama işleminin belirlemek için nokta çizimi
    cv2.putText(frame, "PPL: " + str(ppl), (20, 30), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 255, 0  ), 1, cv2.LINE_AA)
    
    #kişi değeri ilk değerden farklı ise mqtt ile publish et
    if mqttMessage!=ppl:
        mqtt.mqttPublish(ppl)
    mqttMessage=ppl

    frame.flags.writeable = True
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    cv2.imshow('MediaPipe Pose', frame)
    bitis=time.time()
    if cv2.waitKey(1) == ord('q'):
        break

y=np.mean(a)
print("dogruluk: "+str(y))
print(ppl)
print("islem suresi: "+ str(bitis-basla))
cap.release()
if cv2.waitKey(1) == ord('q'):
    cv2.destroyAllWindows()
