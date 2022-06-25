import numpy as np

from skimage import measure
from skimage.io import imread, imsave
from skimage.transform import resize
from skimage.draw import polygon2mask

CLASSES = 3

COLORS = ['black', 'red', 'lime']

SAMPLE_SIZE = (256, 256)

OUTPUT_SIZE = (256, 256)


def detect_teeth(filepath, saving, unet_like):
    frame = imread(f"{filepath}")
    sample = resize(frame, SAMPLE_SIZE)

    predict = unet_like.predict(sample.reshape((1,) + SAMPLE_SIZE + (3,)))
    predict = predict.reshape(SAMPLE_SIZE + (CLASSES,))

    scale = frame.shape[0] / SAMPLE_SIZE[0], frame.shape[1] / SAMPLE_SIZE[1]

    contour_overlay = np.zeros((frame.shape[0], frame.shape[1]))
    contours = measure.find_contours(np.array(predict[:, :, 1]))

    super_mask = np.zeros((frame.shape[0], frame.shape[1], 1), dtype=np.uint8)
    try:
        for contour in contours:
            contour[:, 0] = contour[:, 0] * scale[0]
            contour[:, 1] = contour[:, 1] * scale[1]

            mask = polygon2mask(contour_overlay.shape, contour)

            super_mask[mask] = 1
            print(2)
    except:
        pass
    img_size = frame.shape
    temp = super_mask.copy()

    super_mask = np.append(super_mask, temp, axis=2)
    super_mask = np.append(super_mask, temp, axis=2)

    frame[:, :, 0][super_mask[:, :, 0] != 1] = 0
    frame[:, :, 1][super_mask[:, :, 1] != 1] = 255
    frame[:, :, 2][super_mask[:, :, 2] != 1] = 0

    imsave(f"{filepath.split('.')[0]}_teeth.{filepath.split('.')[-1]}", frame)
    return f"{filepath.split('.')[0]}_teeth.{filepath.split('.')[-1]}"

