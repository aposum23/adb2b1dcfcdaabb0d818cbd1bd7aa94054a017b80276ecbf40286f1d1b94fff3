import cv2
import pickle
from PIL import Image
from cvzone import putTextRect
import os

"""
Teeth AI
"""
check_list = []


def check_karies(processed_img, flag):
    for pos in pos_list:
        x, y = pos
        crop_img = processed_img[y: y + height, x: x + width]
        count = cv2.countNonZero(crop_img)

        if flag == 'rgb':
            if count > 100:
                check_list.append(pos)
                color = (0, 0, 255)
            else:
                color = (0, 255, 0)
        else:
            if count > 83:
                color = (0, 0, 255)
            else:
                color = (0, 255, 0)
        if 0 < len(check_list) < 2 and flag == 'hsv' and pos == check_list[0]:
            color = (0, 0, 255)
            cv2.rectangle(
                img, check_list[0], (check_list[0][0]+width,
                                     check_list[0][1]+height), color, 2
            )
        else:
            if color == (0, 0, 255):

                cv2.rectangle(
                    img, pos, (pos[0] + width, pos[1] + height), color, 2
                )
            else:
                cv2.rectangle(
                    img, pos, (pos[0] + width, pos[1] + height), color, 2
                )


width, height = 73, 60

with open('box_pos', 'rb') as f:
    pos_list = pickle.load(f)

img_name = '6.jpg'

img = cv2.imread(img_name)
img = cv2.resize(img, (256, 256))
putTextRect(img, '1', (2, 30), scale=3, thickness=2, offset=0)
cv2.imshow("orig_img", img)
cv2.waitKey(0)
low_black = (23, 22, 41)
high_black = (35, 70, 100)
processed_karies = cv2.inRange(img, low_black, high_black)
cv2.imshow("processed in rgb!", processed_karies)

check_karies(processed_karies, flag='rgb')

cv2.imshow("img_after_mask", img)
cv2.imwrite('rgb_res.jpg', img)
img = cv2.imread(img_name)
img = cv2.resize(img, (256, 256))
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
cv2.imshow("hsv", img_hsv)
putTextRect(img_hsv, '3', (2, 30), scale=3, thickness=2, offset=0)
cv2.imwrite('hsv_filter.jpg', img_hsv)
hsv_low = (4, 169, 40)
hsv_high = (20, 215, 155)
processed_hsv_karies = cv2.inRange(img_hsv, hsv_low, hsv_high)
cv2.imshow('processed in HSV!', processed_hsv_karies)

check_karies(processed_hsv_karies, flag='hsv')

putTextRect(img, '2', (2, 30), scale=3, thickness=2, offset=0)
cv2.imwrite('hsv_res.jpg', img)
cv2.imshow(f'Discovered hazards!', img)

im_orig = Image.open(img_name)
im1 = Image.open('rgb_res.jpg')
im2 = Image.open('hsv_res.jpg')
im3 = Image.open('hsv_filter.jpg')

combined = Image.new('RGB', (2 * 256, 2 * 256), (250, 250, 250))
combined.paste(im_orig, (0, 0))
combined.paste(im1, (256, 0))
combined.paste(im2, (0, 256))
combined.paste(im3, (256, 256))
combined.show()
combined.save('comb.jpg')
os.remove('rgb_res.jpg')
os.remove('hsv_filter.jpg')
os.remove('hsv_res.jpg')
cv2.waitKey(0)
