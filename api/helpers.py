from django.core.mail import send_mail
from django.conf import settings


def send_forget_password_mail(email, token):
    subject = 'Your Forget Password Link'
    message = 'Hi , Click on the link to reset your password http://127.0.0.1:8000/api/forget_change_pwd/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

def send_admin_forget_password_mail(email):
    subject = 'Your Forget Password Link'
    message = 'Hi , Click on the link to reset your password http://127.0.0.1:8000/api/admin_reset_pwd'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True