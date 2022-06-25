from rest_framework import serializers
from thb.models import Descriptions, Image


class DescrSeerialize(serializers.ModelSerializer):
    class Meta:
        model = Descriptions
        fields = '__all__'


class ImgSerialize(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
