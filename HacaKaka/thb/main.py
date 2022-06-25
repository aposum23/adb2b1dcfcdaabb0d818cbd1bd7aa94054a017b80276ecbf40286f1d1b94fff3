import cv2
import pickle
from PIL import Image
from cvzone import putTextRect
import os
from thb.teeth_detection import detect_teeth, detect_caries

"""
Teeth AI
"""


def process_photo(filepath, unet_like):
    check_list = []

    def check_caries(processed_img, flag):
        if not flag == 'ai':
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
                if 0 < len(check_list) < 2 and flag == 'hsv' and pos == \
                        check_list[
                            0]:
                    color = (0, 0, 255)
                    cv2.rectangle(
                        img, check_list[0], (check_list[0][0] + width,
                                             check_list[0][1] + height), color,
                        2
                    )
                else:
                    if color == (0, 0, 255):

                        cv2.rectangle(
                            img, pos, (pos[0] + width, pos[1] + height), color,
                            2
                        )
                    else:
                        cv2.rectangle(
                            img, pos, (pos[0] + width, pos[1] + height), color,
                            2
                        )
        else:
            for pos in ai_pos_list:
                x, y = pos
                crop_img = processed_img[y: y + ai_height, x: x + ai_width]
                count = cv2.countNonZero(crop_img)
                if count > 37:
                    color = (0, 0, 255)
                else:
                    color = (0, 255, 0)
                cv2.rectangle(
                    img, pos, (pos[0] + ai_width, pos[1] + ai_height), color, 2
                )

    width, height = 73, 60
    ai_width, ai_height = 30, 30

    with open('box_pos', 'rb') as f:
        pos_list = pickle.load(f)

    with open('ai_box_pos', 'rb') as f:
        ai_pos_list = pickle.load(f)

    img_name = filepath

    img = cv2.imread(img_name)
    img = cv2.resize(img, (256, 256))
    putTextRect(img, '1', (2, 30), scale=3, thickness=2, offset=0)
    #cv2.imshow("orig_img", img)
    low_black = (23, 22, 41)
    high_black = (35, 70, 100)
    processed_karies = cv2.inRange(img, low_black, high_black)
    #cv2.imshow("processed in rgb!", processed_karies)

    check_caries(processed_karies, flag='rgb')

    #cv2.imshow("img_after_mask", img)
    cv2.imwrite('rgb_res.jpg', img)

    img = cv2.imread(img_name)
    img = cv2.resize(img, (256, 256))
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    putTextRect(img_hsv, '3', (2, 30), scale=3, thickness=2, offset=0)
    cv2.imwrite('hsv_filter.jpg', img_hsv)
    hsv_low = (4, 169, 40)
    hsv_high = (20, 215, 155)
    processed_hsv_karies = cv2.inRange(img_hsv, hsv_low, hsv_high)

    check_caries(processed_hsv_karies, flag='hsv')

    putTextRect(img, '2', (2, 30), scale=3, thickness=2, offset=0)
    cv2.imwrite('hsv_res.jpg', img)

    img = cv2.imread(img_name)
    img = cv2.resize(img, (256, 256))
    cv2.imwrite(img_name, img)
    teeth_path = detect_teeth(img_name, unet_like)
    teeth = cv2.imread(teeth_path)
    ai_low_black = (10, 11, 20)
    ai_high_black = (37, 40, 150)
    teeth_caries = cv2.inRange(teeth, ai_low_black, ai_high_black)

    check_caries(teeth_caries, flag='ai')
    putTextRect(img, '4', (2, 30), scale=3, thickness=2, offset=0)
    cv2.imwrite('ai_teeth.jpg', img)

    caries_path = detect_caries(img_name, unet_like)
    ai_caries = cv2.imread(caries_path)
    putTextRect(ai_caries, '5', (2, 30), scale=3, thickness=2, offset=0)
    cv2.imwrite('ai_res.jpg', ai_caries)

    im_orig = Image.open(img_name)
    im1 = Image.open('rgb_res.jpg')
    im2 = Image.open('hsv_res.jpg')
    im3 = Image.open('hsv_filter.jpg')
    im4 = Image.open('ai_teeth.jpg')
    im5 = Image.open('ai_res.jpg')

    combined = Image.new('RGB', (2 * 256, 3 * 256), (250, 250, 250))
    combined.paste(im_orig, (0, 0))
    combined.paste(im1, (256, 0))
    combined.paste(im2, (0, 256))
    combined.paste(im3, (256, 256))
    combined.paste(im4, (0, 512))
    combined.paste(im5, (256, 512))
    combined.save('comb.jpg')
    result_path = os.path.abspath('comb.jpg')

    os.remove('rgb_res.jpg')
    os.remove('hsv_filter.jpg')
    os.remove('hsv_res.jpg')
    os.remove(teeth_path)
    os.remove(caries_path)
    os.remove('ai_teeth.jpg')
    os.remove('ai_res.jpg')
    return result_path
