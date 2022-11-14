import math

import cv2
from cvzone.PoseModule import PoseDetector
from cvzone.posemodule1 import PoseDetector1
from threading import Thread
from math import sqrt
video = cv2.VideoCapture(0)
#create a variable that stores the attribute PoseDetector
detect = PoseDetector1()
while 1>0:  #Можно изменить на нажатие какой-то кнопки
    ret,frame = video.read() #ret не нужно, оно проверяет было ли чтение успешным, frame - само изображение
    image_reading = detect.findPose(frame) #getting the position on the image/frame
    body,box_reading = detect.findPosition(frame,bboxWithHands=False)
    #Now, lets check the center of each coordinate in the human body
    if box_reading:
        center = box_reading['center']
        #lets draw and give a crircle mark at each joint movement of the body
        cv2.circle(frame,center,5,(255,255,0),cv2.FILLED)

    color_yellow = (0, 255, 255)
    try:
        distance_between_eyes_pixels = math.sqrt((body[2][2]-body[5][2])**2+(body[2][1]-body[5][1])**2)
        distance_between_eyes_real=60
        frame_real_distance=0.02635872298*frame.shape[0]*1.5
        screen_distance = distance_between_eyes_pixels**(-1.1321)*7301.5525
        angle_shoulders = detect.findAngle(frame,11,12,body[11][2])
        pixel_distance = frame.shape[0]/2-(body[2][2]+body[5][2])/2
        real_distance=distance_between_eyes_real*pixel_distance/distance_between_eyes_pixels
        angle_sitter=math.asin((real_distance+frame_real_distance)/screen_distance)*180/math.pi
        cv2.putText(frame, "head angle " + str(angle_sitter), (30, 150), cv2.FONT_HERSHEY_SIMPLEX, 1,color_yellow, 2)
        cv2.putText(frame, "Shoulders angle " + str(angle_shoulders), (30, 110), cv2.FONT_HERSHEY_SIMPLEX, 1,color_yellow, 2)
        cv2.putText(frame, "Screen distance with aproxy "+str(screen_distance), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color_yellow, 2)
        cv2.putText(frame, "Screen distance with mp "+str((body[2][3]+body[5][3])/2), (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, color_yellow, 2)
        cv2.imshow('frame_name',frame) #показ изображения
    except Exception:
        print("Ну ты и кринж, сядь нормально")
    #если на фото не нашлись нужные нам точки
    if cv2.waitKey(20) and 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()