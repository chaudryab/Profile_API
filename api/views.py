from django.http import response
from django.http.response import HttpResponse, JsonResponse
# from django.shortcuts import render
# from django.contrib.auth.models import auth
from .models import Users,Meetings,Social_links
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
import base64
from django.core.files.base import ContentFile
from uuid import uuid4
# Create your views here.
@csrf_exempt
def users(request):
    if request.method == "POST":
    
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        if Users.objects.filter(email=email).exists():

            data = {}
            data['error'] = 'True'
            data['error_msg'] = 'Email Already Exists!!'
            return JsonResponse(data)

        elif int(len(password)) < 6:
            data = {}
            data['error'] = 'True'
            data['error_msg'] = 'Password must be contain 6 characters!!'
            return JsonResponse(data)
        
        elif name != name.strip():
            data = {}
            data['error'] = 'True'
            data['error_msg'] = 'Name field is required'
            return JsonResponse(data)
        
        elif email != email.strip():
            data = {}
            data['error'] = 'True'
            data['error_msg'] = 'Email field is required'
            return JsonResponse(data)
        
        elif password != password.strip():
            data = {}
            data['error'] = 'True'
            data['error_msg'] = 'Password field is required'
            return JsonResponse(data)

        else:
            user = Users(name=name, email=email, password=password, profession="", phone_no="",address="", image="")
            user.save()
            social = Social_links(user_id=user.pk)
            social.save()
            # user = Users.objects.get(id=user.pk)
        
            data = {}
            data['error'] = 'False'
            data['success_msg'] = 'User created successfully'
            # data['users'] = serializers.serialize("json", [Users.objects.get(id=user.pk)])
            # data['users'] = json.loads(data['users'])
            return JsonResponse(data)
        
            # return HttpResponse(json.dumps(response), content_type="application/json")
            # return JsonResponse(json.dumps(data), content_type="application/json")
            # return JsonResponse(data)
        
 
    else:
        data = {}
        data['error'] = True
        data['error_msg'] = 'Method not supported'
        return JsonResponse(data)
        

@csrf_exempt
def update_profile(request):
    if request.method == "POST":
        user_id = request.POST['user_id']
        name = request.POST['name']
        profession = request.POST['profession']
        address = request.POST['address']
        phone_no = request.POST['phone_no']
        image = request.POST['image']
        # images = base64_to_image(image)


        if Users.objects.filter(id=user_id).exists():
            update = Users.objects.get(id=user_id)

            
            if name != name.strip():
                data = {}
                data['error'] = 'True'
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
                # user = Users.objects.get(id=user.pk)
            
                data = {}
                data['error'] = 'False'
                data['success_msg'] = 'Update successfully'
                data['users'] = serializers.serialize("json", [Users.objects.get(id=update.pk)])
                data['users'] = json.loads(data['users'])
                return JsonResponse(data)
            
                # return HttpResponse(json.dumps(response), content_type="application/json")
                # return JsonResponse(json.dumps(data), content_type="application/json")
                # return JsonResponse(data)
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




@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        # pass = Users.objects.get(password=user.pk)

        if Users.objects.filter(email=email).exists():
            user = Users.objects.get(email=email)
            user_password = user.password
            if password == user_password:
                # p = Users.objects.all()
                # Social_links.objects.all()
                data = {}
                data['error'] = 'False'
                data['success_msg'] = 'Successfully login!!'
                data['users'] = serializers.serialize("json", [Users.objects.get(id=user.pk)])
                data['users'] = json.loads(data['users'])
                data['links'] = serializers.serialize("json", [Social_links.objects.get(user_id=user.pk)])
                data['links'] = json.loads(data['links'])
                user_meetings = Meetings.objects.filter(user_id=user.pk)
                linkss = serializers.serialize('json',user_meetings)
                data["meetings"] = json.loads(linkss)
                print(data)
                return JsonResponse(data)

                # print("yes")
                # data = {}
                # data['error'] = 'False'
                # data['error_msg'] = 'Password Match!!'
                # return JsonResponse(data)
            else:
                data = {}
                data['error'] = 'True'
                data['error_msg'] = 'Password Not Match!!'
                return JsonResponse(data)  
        else:
            data = {}
            data['error'] = 'True'
            data['error_msg'] = 'Email Not Found!!'
            return JsonResponse(data)


        # user = auth.authenticate(email=username, password=password)
        # if user:

        #     if user.is_superuser:
        #         auth.login(request, user)
        #         return redirect('/shop/adminn')

        #     auth.login(request, user)
        #     return redirect('/shop')

        # else:
        #     messages.info(request, 'Invalid Crendentials')
        #     return redirect('/accounts/login')

    else:
        data = {}
        data['error'] = True
        data['error_msg'] = 'Method not supported'
        return JsonResponse(data)

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
            # data['meetings'] = serializers.serialize("json", [Meetings.objects.filter(user_id=user_id).first()])
            # data['meetings'] = json.loads(data['meetings'])
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
            # print(links)
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
                    data['error'] = 'True'
                    data['error_msg'] = 'Password field is required'
                    return JsonResponse(data)
                elif int(len(new_password)) < 6:
                    data = {}
                    data['error'] = 'True'
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