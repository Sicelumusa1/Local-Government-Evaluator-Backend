import random
from django.core.mail import EmailMessage
from .models import Account, OTP
from councilor_rater import settings
from django.core.exceptions import ObjectDoesNotExist

def generateOneTimePin():

    OneTimePin=""
    for i in range(8):
        OneTimePin += str(random.randint(1, 9))
    return OneTimePin

def send_pin(email):
    Subject = 'One time PIN for email verification'
    otp_code = generateOneTimePin()

    try:
        user = Account.objects.get(email=email)
    except ObjectDoesNotExist:
        print("User with email does not exist)")
        return
    email_body = f"Hi {user.first_name} thanks for signing up. \n Please verify your email with the One Time Pin: \n {otp_code}"
    from_email=settings.DEFAULT_FROM_EMAIL

    OTP.objects.create(user=user, pin=otp_code)

    send_email = EmailMessage(subject=Subject, body=email_body, from_email=from_email, to=[email])
    send_email.send(fail_silently=True)