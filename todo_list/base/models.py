from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class list(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    textarea = models.TextField(max_length=300)

    def __str__(self):
        return self.user.username+" "+self.title 