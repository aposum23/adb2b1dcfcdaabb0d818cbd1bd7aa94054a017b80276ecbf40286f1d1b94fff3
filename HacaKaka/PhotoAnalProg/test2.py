from main import process_photo
import os
from cnn import init_cnn


unet_like = init_cnn()

photo_path = os.path.abspath('4.jpg')
resulted_image = process_photo(photo_path, unet_like)
print(resulted_image)
