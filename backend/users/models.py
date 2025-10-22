from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_expires_at = models.DateTimeField(blank=True, null=True)
    otp_purpose = models.CharField(max_length=12, blank=True, null=True)  # 'verify' or 'reset'
    is_verified = models.BooleanField(default=False)
    is_google_account = models.BooleanField(default=False)  # <--- NEW FIELD

    def __str__(self):
        return self.username
