from rest_framework import serializers
from .models import PdfMapping

'''
    Used Django ModelSerializers
'''


class PdfMappingSerializable(serializers.ModelSerializer):
    class Meta:
        model = PdfMapping
        fields = '__all__'
