from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """
    Extended user profile with additional information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    province = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f'Profile for {self.user.username}'
