from django.db import models

# Create your models here.
class paitentmodel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    phoneno = models.IntegerField()
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.email
