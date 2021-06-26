from django.http import response
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Users,Meetings,Social_links
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
import base64
from django.core.files.base import ContentFile
import uuid
from uuid import uuid4
from django.contrib.auth.decorators import login_required
from .helpers import send_forget_password_mail, send_admin_forget_password_mail,send_user_change_email, nfcMail
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import check_password, make_password


# Create your views here.

#------------- User Create --------------
@csrf_exempt
def users(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        if Users.objects.filter(email=email).exists():

            data = {}
            data['error'] = True
            data['error_msg'] = 'Email Already Exists!!'
            return JsonResponse(data)

        elif int(len(password)) < 6:
            data = {}
            data['error'] = True
            data['error_msg'] = 'Password must be contain 6 characters!!'
            return JsonResponse(data)
        
        elif name != name.strip():
            data = {}
            data['error'] = True
            data['error_msg'] = 'Name field is required'
            return JsonResponse(data)
        
        elif email != email.strip():
            data = {}
            data['error'] = True
            data['error_msg'] = 'Email field is required'
            return JsonResponse(data)
        
        elif password != password.strip():
            data = {}
            data['error'] = True
            data['error_msg'] = 'Password field is required'
            return JsonResponse(data)

        else:
            user = Users(name=name, email=email, password=password)
            user.save()
            social = Social_links(user_id=user.pk)
            social.save()        
            data = {}
            data['error'] = 'False'
            data['success_msg'] = 'User created successfully'
            # data['users'] = serializers.serialize("json", [Users.objects.get(id=user.pk)])
            # data['users'] = json.loads(data['users'])
            return JsonResponse(data)
    else:
        data = {}
        data['error'] = True
        data['error_msg'] = 'Method not supported'
        return JsonResponse(data)
        

#------------- User Profile Update --------------
@csrf_exempt
def update_profile(request):
    if request.method == "POST":
        user_id = request.POST['user_id']
        name = request.POST['name']
        profession = request.POST['profession']
        address = request.POST['address']
        phone_no = request.POST['phone_no']
        image = request.POST['image']

        if Users.objects.filter(id=user_id).exists():
            update = Users.objects.get(id=user_id)
            if name != name.strip():
                data = {}
                data['error'] = True
                data['error_msg'] = 'Name field is required'
                return JsonResponse(data)
            else:
                update.name=name
                update.profession=profession
                update.phone_no=phone_no
                update.address=address
                if image != "":
                    images = base64_to_image(image)    
                    update.image=images
                update.save()            
                data = {}
                data['error'] = False
                data['success_msg'] = 'Update successfully'
                data['users'] = serializers.serialize("json", [Users.objects.get(id=update.pk)])
                data['users'] = json.loads(data['users'])
                return JsonResponse(data)
        else:
            data = {}
            data['error'] = 'True'
            data['error_msg'] = 'User Does Not Exists!!'
            return JsonResponse(data)    
    else:
        data = {}
        data['error'] = True
        data['error_msg'] = 'Method not supported'
        return JsonResponse(data)
        
def base64_to_image(base64_string):
    format, imgstr = base64_string.split(';base64,')
    ext = format.split('/')[-1]
    return ContentFile(base64.b64decode(imgstr), name=uuid4().hex + "." + ext)


#------------- User LogIn --------------
@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if Users.objects.filter(email=email).exists():
            user = Users.objects.get(email=email)
            user_password = user.password
            if password == user_password:
                data = {}
                data['error'] = False
                data['success_msg'] = 'Successfully login!!'
                data['users'] = serializers.serialize("json", [Users.objects.get(id=user.pk)])
                data['users'] = json.loads(data['users'])
                data['links'] = serializers.serialize("json", [Social_links.objects.get(user_id=user.pk)])
                data['links'] = json.loads(data['links'])
                user_meetings = Meetings.objects.filter(user_id=user.pk)
                linkss = serializers.serialize('json',user_meetings)
                data["meetings"] = json.loads(linkss)
                return JsonResponse(data)
            else:
                data = {}
                data['error'] = True
                data['error_msg'] = 'Password Not Match!!'
                return JsonResponse(data)  
        else:
            data = {}
            data['error'] = True
            data['error_msg'] = 'Email Not Found!!'
            return JsonResponse(data)
    else:
        data = {}
        data['error'] = True
        data['error_msg'] = 'Method not supported'
        return JsonResponse(data)


#------------- User Meetings --------------
@csrf_exempt
def meetings(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        link = request.POST['link']
        if Users.objects.filter(id=user_id).exists():
            meeting = Meetings(user_id=user_id,link=link)
            meeting.save()
            data = {}
            data['error'] = False
            data['success_msg'] = 'Meeting Saved!!'
            user_meetings = Meetings.objects.filter(user_id=user_id)
            linkss = serializers.serialize('json',user_meetings)
            data["meetings"] = json.loads(linkss)
            return JsonResponse(data)
        else:
            data = {}
            data['error'] = True
            data['error_msg'] = 'User Not Found!!'
            return JsonResponse(data)
    else:
        data = {}
        data['error'] = True
        data['error_msg'] = 'Method not supported'
        return JsonResponse(data)


#------------- User Social Links --------------
@csrf_exempt
def social_links(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        fb = request.POST['fb']
        insta = request.POST['insta']
        linkedin = request.POST['linkedin']
        youtube = request.POST['youtube']

        if Users.objects.filter(id=user_id).exists():
            links = Social_links.objects.get(user_id=user_id)
            links.fb=fb
            links.insta=insta
            links.linkedin=linkedin
            links.youtube=youtube
            links.save()
            data = {}
            data['error'] = False
            data['success_msg'] = 'Social Links Saved!!'
            data['links'] = serializers.serialize("json", [Social_links.objects.get(user_id=user_id)])
            data['links'] = json.loads(data['links'])
            return JsonResponse(data) 
        else:
            data = {}
            data['error'] = True
            data['error_msg'] = 'User Not Found!!'
            return JsonResponse(data)
    else:
        data = {}
        data['error'] = True
        data['error_msg'] = 'Method not supported'
        return JsonResponse(data)


#------------- User Password Change in Profile --------------
@csrf_exempt
def change_password(request):
    if request.method == "POST":
        user_id = request.POST['user_id']
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']

        if Users.objects.filter(id=user_id).exists():
            user = Users.objects.get(id=user_id)
            if user.password == old_password:
                if new_password != new_password.strip():
                    data = {}
                    data['error'] = True
                    data['error_msg'] = 'Password field is required'
                    return JsonResponse(data)
                elif int(len(new_password)) < 6:
                    data = {}
                    data['error'] = True
                    data['error_msg'] = 'Password must be contain 6 characters!!'
                    return JsonResponse(data)
                else:
                    user.password=new_password
                    user.save()
                    data = {}
                    data['error'] = False
                    data['success_msg'] = 'Password Changed'
                    return JsonResponse(data)
            else:
                data = {}
                data['error'] = True
                data['error_msg'] = 'Old Password Not Match!!!'
                return JsonResponse(data)
        else:
            data = {}
            data['error'] = True
            data['error_msg'] = 'User Not Found!!!'
            return JsonResponse(data)
    else:
        data = {}
        data['error'] = True
        data['error_msg'] = 'Method not supported'
        return JsonResponse(data)


#------------- Admin LogIn --------------
@csrf_exempt
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user:

            if user.is_superuser:
                auth.login(request, user)
                return redirect('index')
        else:
            messages.info(request, 'Invalid Crendentials')
            return redirect('admin_login')
    else:
        return render(request, 'login.html')


#------------- Reterive Dashboard In Admin Panel --------------
@login_required
def index(request):
    return render(request, 'index.html')


#------------- Reterive All Users In Admin Panel --------------
@login_required
def customers(request):
    data = Users.objects.all()
    cus = {"username": data}
    return render(request, 'users.html',cus)


#------------- Reterive ##### In Admin Panel --------------
@login_required
def c_meetings(request):
    return render(request, 'meetings.html')


#------------- Admin Logout --------------
@login_required
def logout(request):
    auth.logout(request)
    return redirect('admin_login')


#------------- Admin Change Password --------------
@login_required
@csrf_exempt
def admin_change_pwd(request):
    superusers = User.objects.get(is_superuser=True)
    print(superusers.password)

    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        superusers = User.objects.get(is_superuser=True)
        if check_password(old_password,superusers.password):
            if int(len(new_password)) < 6:
                messages.info(request, 'Password Must Contains Six Characters!!')
                return redirect('admin_change_pwd')
            elif new_password == confirm_password:
                super_pwd = make_password(new_password, None, 'md5')
                superusers.password = super_pwd
                superusers.save()
                messages.info(request, 'Password Changed!!')
                return redirect('admin_change_pwd')
            else:
                messages.info(request, 'Password Did Not Match!!')
                return redirect('admin_change_pwd')
        else:
            messages.info(request, 'Invalid Old Password!!')
            return redirect('admin_change_pwd')

    return render(request,'admin_change_pwd.html')


#------------- Reterive Specific User Detail In Admin Panel --------------
@login_required
def user_detail(request,pk):
    data = Users.objects.filter(id=pk)
    data1 = Meetings.objects.filter(user_id=pk)
    data2 = Social_links.objects.filter(user_id=pk)
    cus_detail = {"user_detail": data,"user_meetings": data1,"user_socialLinks": data2}
    return render(request, 'user_detail.html', cus_detail)


#------------- Delete Specific User In Admin Panel --------------
@login_required
def user_delete(request, pk):
    instance_user = Users.objects.filter(id=pk)
    instance_user.delete()
    instance_links = Social_links.objects.filter(user_id=pk)
    instance_links.delete()
    instance_meetings = Meetings.objects.filter(user_id=pk)
    instance_meetings.delete()
    return redirect('customers')


#------------- Admin Forget Password --------------
@csrf_exempt
def admin_forget_pwd(request):
    if request.method == 'POST':
        email = request.POST['email']
        superuser = User.objects.get(is_superuser=True)
        print(superuser)
        print(email)
        if superuser.email == email:
            send_admin_forget_password_mail(email)
            messages.info(request, 'Email Send!!')
            return redirect('admin_forget_pwd')
        else:
            messages.info(request, 'Email Not Exist!!')
            return redirect('admin_forget_pwd')

    return render(request,'admin_forget_pwd.html')


#------------- User Forget Password --------------
@csrf_exempt
def forget_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Users.objects.filter(email=email):
            token = str(uuid.uuid4())
            user = Users.objects.get(email=email)
            user.forget_password_token=token
            user.save()
            email=user.email
            send_forget_password_mail(email, token)
            data = {}
            data['error'] = False
            data['success_msg'] = 'Email Send!!!'
            return JsonResponse(data)
        else:
            data = {}
            data['error'] = True
            data['error_msg'] = 'Email Not Exist!!'
            return JsonResponse(data)
    else:
        data = {}
        data['error'] = True
        data['error_msg'] = 'Method not supported'
        return JsonResponse(data)


#------------- Admin Change Forget Password --------------
@csrf_exempt
def admin_reset_pwd(request):
    if request.method == 'POST':
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        superusers = User.objects.get(is_superuser=True)
        if int(len(new_password)) < 6:
            messages.info(request, 'Password Must Contains Six Characters!!')
            return redirect('admin_reset_pwd')
        elif new_password == confirm_password:
            super_pwd = make_password(new_password, None, 'md5')
            superusers.password = super_pwd
            superusers.save()
            messages.info(request, 'Password Changed!!')
            return redirect('admin_reset_pwd')
        else:
            messages.info(request, 'Password Did Not Match!!')
            return redirect('admin_reset_pwd')
    return render(request, 'admin_reset_pwd.html')

#------------- User Change Forget Password --------------
@csrf_exempt
def forget_change_pwd(request,token):
    if request.method == 'GET':
        user = Users.objects.filter(forget_password_token = token).first()
        if user:
            return render(request, 'forget_change_pwd.html', {'token': token, 'user_id': user.id})
        else:
            return render(request,"404_error.html")
    if request.method == 'POST':
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        user_id = request.POST['user_id']
        if new_password != confirm_password:
            messages.info(request, 'Password Not Match!!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
        elif int(len(new_password)) < 6:
            messages.info(request, 'Password Must Be Contain Six Characters!!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
        else:
            user=Users.objects.get(id=user_id)
            print(user)
            # pwd = make_password(new_password, None, 'md5')
            user.password=new_password
            user.forget_password_token=''
            user.save()
            data = {}
            return redirect('success')

    return render(request, 'forget_change_pwd.html')


#------------- Succsess Message Page After Change Password --------------
def success(request):
    return render(request, 'success.html')


#------------- Scan NFC User Profile Page  --------------
def myprofile(request,id):
    if request.method == "GET":
        if Users.objects.filter(id=id):
            user=Users.objects.get(id=id)
            links=Social_links.objects.get(user_id=id)
            return render(request,'myprofile.html', {'user':user, 'links':links})
        else:
            return render(request,'404_error.html')
    else:
        return render(request,'404_error.html')


#------------- Send Mail To NFC User Profile Page  --------------
@csrf_exempt
def nfc_mail(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        sentto = request.POST['sentto']
        nfcMail(name,email,subject,message,sentto) 
        return render(request,'myprofile.html')
    else:   
        return render(request,'myprofile.html')


#------------- Send User Change Email  --------------
@csrf_exempt
def user_send_change_email(request):
    if request.method == "POST":
        user_id = request.POST['user_id']
        new_email = request.POST['new_email']
        password = request.POST['password']
        
        if Users.objects.filter(id=user_id):
            user = Users.objects.get(id=user_id)
            if password == user.password:
                
                if Users.objects.filter(email = new_email).exists():
                    if user.email == new_email :
                        data = {}
                        data['error'] = True
                        data['error_msg'] = 'Email already in your use'
                        return JsonResponse(data)
                    else:
                        data = {}
                        data['error'] = True
                        data['error_msg'] = 'Email already exists'
                        return JsonResponse(data)
                else:
                    token = str(uuid.uuid4())
                    user.forget_password_token = token
                    user.save()
                    send_user_change_email(new_email, token)
                    data = {}
                    data['error'] = False
                    data['success_msg'] = 'Email sent successfully'
                    return JsonResponse(data)
                    
            else:
                data = {}
                data['error'] = True
                data['error_msg'] = 'password not match'
                return JsonResponse(data) 
        else:
            data = {}
            data['error'] = True
            data['error_msg'] = 'User not found'
            return JsonResponse(data) 
    else:
        data = {}
        data['error'] = True
        data['error_msg'] = 'Method not supported'
        return JsonResponse(data)


#------------- User Change Email  --------------
@csrf_exempt
def user_change_email(request, token, email):
    if request.method == 'GET':
        if Users.objects.filter(forget_password_token = token).exists():
            user = Users.objects.filter(forget_password_token=token).first()
            user.email = email
            user.forget_password_token = ''
            user.save()
            return render(request, 'success_email.html',{'token': token, 'email': email})
        else:
            return render(request, '404_error.html')
    else:
        return render(request, '404_error.html')
