from django.db import models

class Storage(models.Model):
    name = models.CharField(max_length=255)
    uploader = models.ForeignKey('authentication.Employee', on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
