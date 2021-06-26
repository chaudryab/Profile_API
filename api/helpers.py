from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.template import loader
import smtplib



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

def nfcMail(name,email,subject,message,sentto):
    html_message = render_to_string('profile_msg.html', {'name':name,'email': email,'subject':subject,'message':message})
    plain_message = strip_tags(html_message)
    email_from = 'alijutt64672@gmail.com'
    recipient_list = [sentto]
    send_mail(subject, plain_message, email_from, recipient_list, html_message=html_message)

    # host = "server.smtp.com"
    # server = smtplib.SMTP(host, 587)
    # FROM = "abchaudry9@gmail.com"
    # TO = "saadmb1995@gmail.com"
    # MSG = "Subject: Test email python\n\nBody of your message!"
    # server.sendmail(FROM, TO, MSG)

    # server.quit()
    # print ("Email Send")

    # sender = 'saadmb1995@gmail.com'
    # receivers = ['alijutt46472@gmail.com']

    # message = """From: No Reply <no_reply@mydomain.com>
    # To: Person <person@otherdomain.com>
    # Subject: Test Email

    # This is a test e-mail message.
    # """

    # try:
    #     smtpObj = smtplib.SMTP(host='localhost', port="8000")
    #     smtpObj.sendmail(sender, receivers, message)         
    #     print("Successfully sent email")
    # except SMTPException:
    #     print("Error: unable to send email")
    return True
  