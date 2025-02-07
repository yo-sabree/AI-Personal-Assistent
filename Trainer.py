import cv2
import mediapipe as mp

pushup = cv2.VideoCapture("Pushup.mp4")

"""
Pushup - Shoulder above hand elbow (Shoulder - [11,12], Hand Elbow - [13,14])
"""

pullup = cv2.VideoCapture("Pullup.mp4")

"""
Pullup - Shoulder below hand elbow (Shoulder - [11,12], Hand Elbow - [13,14])
"""

squat = cv2.VideoCapture("Squat.mp4")

"""
Squat - Hip near straight to leg elbow (Hip - [23,24], Hand Leg Elbow - [25,26])
"""

benchpress = cv2.VideoCapture("Bench Press.mp4")

"""
BenchPress - Hand Elbow below shoulder (Shoulder - [11,12], Hand Elbow - [13,14])
"""

mppose = mp.solutions.pose
pose = mppose.Pose()

mpdraw = mp.solutions.drawing_utils

cTime = 0
pTime = 0

while True:
    success, img = benchpress.read()
    cvtimg = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    poses = pose.process(cvtimg)
    if poses.pose_landmarks:
        mpdraw.draw_landmarks(img,poses.pose_landmarks,mppose.POSE_CONNECTIONS)
        for id, lm in enumerate(poses.pose_landmarks.landmark):
            h,w,c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(img,(cx,cy),2,(0,255,0),cv2.FILLED)

    cv2.imshow("Pose",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
