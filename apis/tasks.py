from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
import random
from datetime import timedelta
from config import settings

@shared_task
def send_otp_email(email):
    otp = generate_otp()
    expiration_time = timezone.now() + timedelta(minutes=10)  # Adjust the expiration time as needed

    send_otp_to_user(email, otp)
    return otp, expiration_time

def generate_otp():
    otp = str(random.randint(100000, 999999))
    return otp


def send_otp_to_user(email, otp):
    subject = 'Your OTP for Login'
    message = f'Your OTP for login is: {otp}. This OTP is valid for a limited time.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

