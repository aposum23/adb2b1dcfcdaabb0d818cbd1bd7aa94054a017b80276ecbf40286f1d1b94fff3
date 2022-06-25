import cv2
import pickle
import cvzone
import numpy as np

"""
Teeth AI
"""
check_list = []


def check_karies(processed_img, flag):
    controversial = False
    print(pos_list)
    for pos in pos_list:
        x, y = pos
        crop_img = processed_img[y: y + height, x: x + width]
        cv2.imshow(str(x * y) + flag, crop_img)
        count = cv2.countNonZero(crop_img)
        cvzone.putTextRect(
            img, str(count), (x, y + height - 3), scale=1, thickness=1,
            offset=0
                           )

        if flag == 'rgb':
            if count > 100:
                check_list.append(pos)
                color = (0, 0, 255)
            else:
                color = (0, 255, 0)
        else:
            if count > 90 and pos in check_list:
                color = (0, 0, 255)
            else:
                color = (0, 255, 0)
        print(check_list)
        if 0 < len(check_list) < 2 and flag == 'hsv' and pos == check_list[0]:
            color = (0, 0, 255)
            cv2.rectangle(
                img, check_list[0], (check_list[0][0]+width,
                                     check_list[0][1]+height), color, 2
            )
            controversial = True
        else:
            cv2.rectangle(img, pos, (pos[0] + width,pos[1] + height), color, 2)

    return controversial


width, height = 73, 60

with open('box_pos', 'rb') as f:
    pos_list = pickle.load(f)

img_name = '1src.jpg'

img = cv2.imread(img_name)
cv2.imshow("orig_img", img)
cv2.waitKey(0)
# img_crop = img[23:211, 20:230]
# img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# cv2.imshow("hsv", img_hsv)
low_black = (23, 15, 41)
high_black = (50, 70, 100)
processed_karies = cv2.inRange(img, low_black, high_black)
cv2.imshow("processed in rgb!", processed_karies)

contr_sit = check_karies(processed_karies, flag='rgb')

cv2.imshow("img_after_mask", img)

img = cv2.imread(img_name)
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
cv2.imshow("hsv", img_hsv)
low_black = (4, 169, 40)
high_black = (20, 205, 155)
processed_hsv_karies = cv2.inRange(img_hsv, low_black, high_black)
cv2.imshow('processed in HSV!', processed_hsv_karies)
contr_sit = check_karies(processed_hsv_karies, flag='hsv')
if contr_sit:
    print("СПОРНАЯ СИТУАЦИЯ")
    cv2.imshow('Controversial situation', img)
else:
    cv2.imshow('img after HSV', img)
cv2.waitKey(0)

"""
backup 
low_black = (7, 0, 10)
high_black = (108, 98, 89)
"""

"""
backup hsv horoshee
low_black = (17, 80, 40)
high_black = (20, 205, 155)
"""
"""
hsv dlya nalogenia?
low_black = (15, 80, 40)
high_black = (20, 205, 155)
"""