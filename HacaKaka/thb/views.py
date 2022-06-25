from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from thb.models import Descriptions, Image
from thb.serializers import DescrSeerialize, ImgSerialize
import cv2
import pickle
import cvzone
import base64
import numpy as np
import json

def checkImg(img_inp):
    img = cv2.imread(f'image/{img_inp}')


class PhotoAnal(APIView):
    def post(self, request):
        print('HacaKaka')
        file = request.FILES['photo']
        photo = Image.objects.filter(name=file.name)
        photo.delete()
        print(type(file))
        print(file)
        Image.objects.create(img=file, name=file.name)
        img = Image.objects.filter(name=file.name)
        print(img)
        checkImg(file.name)
        photo = Image.objects.filter(name=file.name)
        ser = ImgSerialize(photo, many=True)
        return HttpResponse(photo[0].img, content_type='image/jpeg')
