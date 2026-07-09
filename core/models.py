from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profiles/', default='default.png')
    contact = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username
