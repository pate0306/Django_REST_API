"""Django_REST_API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from Django_REST_API import view

urlpatterns = [
    path('admin/', admin.site.urls),  # To open admin panel in the browser
    path('api-token-auth/', obtain_auth_token),  # To obtain a token given the username and password as data
    path('pdf_list/', view.PdfListView.as_view()),  # To add the PdfList - passing the file and password to encrpyt it with
    path('download_pdf_file/', view.PdfDownloadView.as_view())  # To download the pdf file - passing pdf_name
]
