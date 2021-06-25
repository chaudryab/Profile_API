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
from .helpers import send_forget_password_mail, send_admin_forget_password_mail
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


#------------- Admin Logout --------------
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


#------------- Forget Password --------------
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

#------------- Change Forget Password --------------
@csrf_exempt
def forget_change_pwd(request,token):
    if request.method == 'GET':
        user = Users.objects.get(forget_password_token = token)
        return render(request, 'forget_change_pwd.html', {'token': token, 'user_id': user.id})
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

def success(request):
    return render(request, 'success.html')
    
def myprofile(request):
    return render(request,'myprofile.html')
# #------------------------------------------------------------------------------------------

# from django.contrib.auth.hashers import check_password, make_password
# def change_password(request, token):
#     if request.method == 'GET':
#         user = Users.objects.get(forget_password_token = token)
#         return render(request, 'api/Forgotten_psw.html', {'token': token, 'user_id': user.id})
#         
#     if request.method == 'POST':
#         user = Users.objects.get(forget_password_token = token)
#         password = request.POST['password']
#         confirm_password = request.POST['confirm_password']
#         user_id = request.POST['user_id']
#         if user_id is None:
#             data = {}
#             data['error'] = True
#             data['error_msg'] = 'No user id found'
#             return JsonResponse(data)
#         if password != confirm_password:
#             data = {}
#             data['error'] = True
#             data['error_msg'] = 'password should be same'
#             return JsonResponse(data)
        
#         userrr = Users.objects.get(id = user_id)
#         pwd = make_password(password, None, 'md5')
#         userrr.password = pwd
#         # print(userrr.forget_password_token)
#         userrr.forget_password_token = ''
#         userrr.save()
        
#         data = {}
#         data['error'] = False
#         data['success_msg'] = 'New Password saved!'
#         return JsonResponse(data)
                
  

#     return render(request, 'api/Forgotten_pswd.html')


# from django.core.mail import send_mail

# @csrf_exempt
# def forget_password(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         if not Users.objects.filter(email=email).first():
#             data = {}
#             data['error'] = True
#             data['error_msg'] = 'User not found with this email'
#             return JsonResponse(data)
#         user_obj = Users.objects.filter(email=email).first()
#         email = user_obj.email
#         token = str(uuid.uuid4())
#         user_obj.forget_password_token = token
#         user_obj.save()
#         send_forget_password_mail(email, token)
#         data = {}
#         data['error'] = False
#         data['success_msg'] = 'email sent!'
#         return JsonResponse(data)    
#     else:
#         return HttpResponse('Forgot Password Not Supported')

