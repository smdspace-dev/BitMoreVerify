import random
from datetime import timedelta
from django.utils import timezone

def generate_otp():
    return str(random.randint(100000, 999999))

def set_otp(user, purpose="verify", minutes_valid=10):
    user.otp = generate_otp()
    user.otp_purpose = purpose
    user.otp_expires_at = timezone.now() + timedelta(minutes=minutes_valid)
    user.save(update_fields=["otp", "otp_purpose", "otp_expires_at"])
    return user.otp

def otp_is_valid(user, otp, purpose):
    if not (user.otp and user.otp_expires_at and user.otp_purpose):
        return False
    if user.otp != otp:
        return False
    if user.otp_purpose != purpose:
        return False
    if timezone.now() > user.otp_expires_at:
        return False
    return True
