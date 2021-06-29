from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.template import loader


def send_forget_password_mail(email, token):
    subject = 'Your Forget Password Link'
    message = 'Hi , Click on the link to reset your password http://127.0.0.1:8000/api/forget_change_pwd/'+token
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

def send_user_change_email(email, token):
    link = 'http://127.0.0.1:8000/api/user_change_email/'+token+'/'+email
    subject = 'your change email link'
    html_message = render_to_string('mail_template.html', {'link': link})
    plain_message = strip_tags(html_message)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, plain_message, email_from, recipient_list, html_message=html_message)
    return True

def send_admin_forget_password_mail(email):
    subject = 'Your Forget Password Link'
    message = 'Hi , Click on the link to reset your password http://127.0.0.1:8000/api/admin_reset_pwd'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

