from rest_framework.views import APIView
from django.http import HttpResponse
from thb.models import Descriptions, Image
from thb.serializers import DescrSeerialize, ImgSerialize
from thb.main import process_photo
from HacaKaka.manage import unet_like
import cv2
import base64
import os


def image_as_base64(image_file, format='jpeg'):
    """
    :param `image_file` for the complete path of image.
    :param `format` is format for image, eg: `png` or `jpg`.
    """
    if not os.path.isfile(image_file):
        return None

    encoded_string = ''
    with open(image_file, 'rb') as img_f:
        encoded_string = base64.b64encode(img_f.read())
    return 'data:image/%s;base64,%s' % (format, encoded_string)


class PhotoAnal(APIView):
    def post(self, request):
        file = request.FILES['photo']
        photo = Image.objects.filter(name=file.name)
        photo.delete()
        Image.objects.create(img=file, name=file.name)
        img = Image.objects.filter(name=file.name)
        file_path = './media/' + img[0].img.name

        result_path = process_photo(file_path, unet_like)

        base64_photo = image_as_base64(result_path)

        os.remove(result_path)
        img.delete()
        os.remove(file_path)

        return HttpResponse(base64_photo, content_type='image/jpeg')
