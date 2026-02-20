from django.db import models

# Create your models here.

class Travel(models.Model):
    has_traveled_toeurope= models.BooleanField(default=False)
    contries=models.JSONField(null=True, blank=True)
    