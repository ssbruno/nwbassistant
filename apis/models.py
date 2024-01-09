from django.db import models

# Create your models here.
class AssistantResponse(models.Model):
    text_rsp = models.CharField(max_length=2000)
    audio_rsp = models.CharField(max_length=4000)