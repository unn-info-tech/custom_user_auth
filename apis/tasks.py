from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
import random
from datetime import timedelta
from config import settings
from django.core.cache import cache
import time

@shared_task
def generate_otp():
    return str(random.randint(100000, 999999))

def generate_and_store_otp(email):
    otp = generate_otp()
    expiration_time = 300  # OTP expires in 5 minutes (300 seconds)
    current_timestamp = int(time.time())
    cache_key = f"otp_{email}"
    cache.set(cache_key, {'otp': otp, 'timestamp': current_timestamp}, expiration_time)
    return otp

def send_otp_email(email, otp):
    subject = 'Your OTP for Login'
    message = f'Your OTP for login is: {otp}. This OTP is valid for a limited time.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

