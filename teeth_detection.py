import numpy as np
import cv2
import skimage.io

from skimage import measure
from skimage.io import imread, imsave, imshow
from skimage.transform import resize
from skimage.filters import gaussian
from skimage.morphology import dilation, disk
from skimage.draw import polygon, polygon_perimeter, polygon2mask
import matplotlib.pyplot as plt

CLASSES = 3

COLORS = ['black', 'red', 'lime']

rgb_colors = [
    (0,   0,   0),
    (255, 0,   0),
    (0, 58, 255),
    (0,   0,   255),
    (255, 165, 0),
    (255, 192, 203),
    (0,   255, 255),
    (255, 0,   255)
]

SAMPLE_SIZE = (256, 256)

OUTPUT_SIZE = (256, 256)


def detect_caries(filepath, unet_like):
    frame = imread(f"{filepath}")
    sample = resize(frame, SAMPLE_SIZE)

    predict = unet_like.predict(sample.reshape((1,) + SAMPLE_SIZE + (3,)))
    predict = predict.reshape(SAMPLE_SIZE + (CLASSES,))

    scale = frame.shape[0] / SAMPLE_SIZE[0], frame.shape[1] / SAMPLE_SIZE[1]

    contour_overlay = np.zeros((frame.shape[0], frame.shape[1]))
    contours = measure.find_contours(np.array(predict[:, :, 2]))

    try:
        for contour in contours:
            rr, cc = polygon_perimeter(contour[:, 0] * scale[0],
                                       contour[:, 1] * scale[1],
                                       shape=contour_overlay.shape)

            contour_overlay[rr, cc] = 1

        contour_overlay = dilation(contour_overlay, disk(1))
        frame[contour_overlay == 1] = rgb_colors[2]
    except:
        pass
    #plt.imshow(frame)
    #plt.show()
    print(f"{filepath.split('.')[0]}_caries.{filepath.split('.')[-1]}")
    imsave(f"{filepath.split('.')[0]}_caries.{filepath.split('.')[-1]}", frame)
    return f"{filepath.split('.')[0]}_caries.{filepath.split('.')[-1]}"


def detect_teeth(filepath, unet_like):
    frame = skimage.io.imread(f"{filepath}")
    sample = resize(frame, SAMPLE_SIZE)

    predict = unet_like.predict(sample.reshape((1,) + SAMPLE_SIZE + (3,)))
    predict = predict.reshape(SAMPLE_SIZE + (CLASSES,))

    scale = frame.shape[0] / SAMPLE_SIZE[0], frame.shape[1] / SAMPLE_SIZE[1]
    super_mask = np.zeros((frame.shape[0], frame.shape[1], 1), dtype=np.uint8)

    for channel in range(1, CLASSES):
        contour_overlay = np.zeros((frame.shape[0], frame.shape[1]))
        contours = measure.find_contours(np.array(predict[:, :, channel]))
        try:
            for contour in contours:
                contour[:, 0] = contour[:, 0] * scale[0]
                contour[:, 1] = contour[:, 1] * scale[1]

                mask = polygon2mask(contour_overlay.shape, contour)

                super_mask[mask] = 1
        except:
            pass
    temp = super_mask.copy()

    super_mask = np.append(super_mask, temp, axis=2)
    super_mask = np.append(super_mask, temp, axis=2)

    frame[:, :, 0][super_mask[:, :, 0] != 1] = 0
    frame[:, :, 1][super_mask[:, :, 1] != 1] = 255
    frame[:, :, 2][super_mask[:, :, 2] != 1] = 0

    imsave(f"{filepath.split('.')[0]}_teeth.{filepath.split('.')[-1]}", frame)
    print("DONE!")
    return f"{filepath.split('.')[0]}_teeth.{filepath.split('.')[-1]}"
