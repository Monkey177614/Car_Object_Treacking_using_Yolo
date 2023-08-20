import cv2
import numpy as np
from object_detection import ObjectDetection
import math

# OBJECT DETECTION PART

od = ObjectDetection()

# Input video
cap = cv2.VideoCapture("Trafice Video.mp4")

count = 0
center_point_prev_frame = []
tracking_object = {}
track_id = 0

while True:
    rat, frame = cap.read()  # frame is frame
    count += 1  # Start count the object number
    if not rat:  # this one is Frame ture or false
        break

    center_point_car_frame = []

    # detect object on frame
    class_ids, scores, boxes = od.detect(frame)  # cass_ids = get a objetct , boxes = make a box on the object , se\cored  =  how much cobject  has
    for box in boxes:
        # print(box) # just print how many object detect
        (x, y, h, w) = box
        cx = int((x + x + w) / 2)  # canter point of the box  calculate x =x1, x+w =x2 so result is x+x+w/2 =(x1+(x2+w))
        cy = int((y + y + w) / 2)  # same mathow ithe cx
        center_point_car_frame.append((cx, cy))  # get the object data

        # print("FRAME NUMBER :", count, "", x, y, w, h)  # count the box  with  object

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if count <= 1:
        for pt in center_point_car_frame:
            for pt2 in center_point_prev_frame:
                distance = math.hypot(pt2[0] - pt[0], pt2[-1] - pt[1])

                if distance < 20:
                    tracking_object[track_id] = pt
                    track_id += 1  # count the tracking object
    else:
        tracking_object_copy = tracking_object.copy()

        for object_id, pt2 in tracking_object_copy.items():

            object_exists = False
            for pt in center_point_car_frame:

                distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])
                # update object  postion

                if distance < 20:  # Id position
                    tracking_object[object_id] = pt
                    object_exists = True
                    if pt in center_point_car_frame:
                        center_point_car_frame.remove(pt)
                    continue

            # Remove id
            if not object_exists:
                tracking_object.pop(object_id)

    for pt in center_point_car_frame:  # Add new id lost
        tracking_object[track_id] = pt
        track_id += 1

    for object_id, pt in tracking_object.items():
        cv2.circle(frame, pt, 5, (0, 0, 255), -1)  # make ac circle  color
        cv2.putText(frame, str(object_id), (pt[0], pt[1] - 7), 0, 1, (0, 0, 255), 2)

    print(tracking_object)
    cv2.imshow("Frame", frame)

    print("CUR FRAME LEFT PTS")
    print(center_point_car_frame)

    center_point_prev_frame = center_point_car_frame.copy()

    key = cv2.waitKey(0)  # it is movieing 1  mili secend
    if key == 27:
        break
cap.release()
cv2.destoryAllwindows()

#%%
