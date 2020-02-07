from django.contrib.auth.models import User
from django.db import models


# PdfMapping database model
class PdfMapping(models.Model):
    pdf_name = models.TextField(null=False, default='')
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
