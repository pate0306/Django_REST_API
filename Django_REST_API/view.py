from django.http import HttpResponse
from .models import PdfMapping
from .serializable import PdfMappingSerializable
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
import PyPDF2 as p, os
from rest_framework.status import (HTTP_400_BAD_REQUEST, HTTP_200_OK)
from wsgiref.util import FileWrapper

'''
    Super User password
'''
DEFAULT_PDF_OWNER_PASSWORD = "admin"

'''
    Need to use different keyword in the header, such as Bearer. So,subclass TokenAuthentication and set the keyword class variable.
'''


class BearerAuthentication(TokenAuthentication):
    keyword = 'Bearer'


'''
    
'''


class PdfListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BearerAuthentication,)

    def get(self, request):
        if is_admin(request.user):
            pdfs = PdfMapping.objects.all()
        else:
            pdfs = PdfMapping.objects.filter(user_id=request.user.id)
        serializer = PdfMappingSerializable(pdfs, many=True)

        return Response(serializer.data)

    '''
            Uploading the Pdf by using Password and File obj
    '''

    def post(self, request):
        password = request.POST['password']
        file_obj = request.FILES['file']

        try:
            file_name = encrypt_and_save_file(file=file_obj, password=password, user_id=request.user.id)
            PdfMapping.objects.create(pdf_name=file_name, user=request.user)
        except FileNotFoundError:
            return Response({'error': 'Unable to Open file.'}, status=HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'error': 'User id not found. Please try again'}, status=HTTP_400_BAD_REQUEST)

        return Response({'msg': 'File upload successful'}, status=HTTP_200_OK)


'''
    PdfDownloadView class use to Download the pdf by using Pdf name
'''


class PdfDownloadView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BearerAuthentication,)

    def get(self, request):
        pdf_name = None
        try:
            pdf_name = request.data['pdf_name']
            if pdf_name is None:
                raise FileNotFoundError
        except FileNotFoundError:
            return Response({'error': 'pdf_name parameter is missing from request. Please add one.'}, status=HTTP_400_BAD_REQUEST)
        try:
            file_path = 'media/' + str(request.user.id) + '/' + pdf_name
            short_report = open(file_path, 'rb')
        except FileNotFoundError:
            return Response({'error': 'Unable to find file with the name in request. Please correct the name and try again.'}, status=HTTP_400_BAD_REQUEST)

        response = HttpResponse(FileWrapper(short_report), content_type='application/pdf')

        return response


'''
    To check that user is admin (Super User) or not
'''


def is_admin(user):
    return user.is_superuser


'''
    User to encrypt and save file to server (currently in media directory by default) can change by
    passing it as argument to the function
'''


def encrypt_and_save_file(file=None, root_folder_name='media', user_id=None, password='password'):
    if file is None:
        raise FileNotFoundError

    if user_id is None:
        raise Exception

    output = p.PdfFileWriter()
    # read the Pdf file
    input_stream = p.PdfFileReader(file)

    for i in range(0, input_stream.getNumPages()):
        output.addPage(input_stream.getPage(i))
    # Declare the pdf file path
    file_path = root_folder_name + '/' + str(user_id) + '/' + file.name
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    output_stream = open(file_path, "wb")
    # encrypt the Pdf by using current user password, admin password
    output.encrypt(user_pwd=password, owner_pwd=DEFAULT_PDF_OWNER_PASSWORD, use_128bit=True)
    output.write(output_stream)
    output_stream.close()

    return file.name
