from django.shortcuts import render,redirect
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from random import randrange
# Create your views here.


def llogin(request):
    try:
        lab = Assistants.objects.get(email=request.session['email'])
        return render(request,'ldash.html',{'lab':lab})
    except:
        if request.method == 'POST':
            try:
                lab = Assistants.objects.get(email=request.POST['email'])
                if request.POST['password'] == lab.password:
                    request.session['email'] = request.POST['email']
                    return render(request,'ldash.html',{'lab':lab})
                return render(request,'llogin.html',{'msg':'Inncorrect password','lab':lab})
            except:
                msg = 'Email is not register'
                return render(request,'llogin.html',{'msg':msg,'lab':lab})
        return render(request,'llogin.html')



def llogout(request):
    del request.session['email']
    return render(request,'llogin.html') 
    
def ledit(request):
    lab = Assistants.objects.get(email=request.session['email'])
    if request.method == 'POST':
        lab.name = request.POST['name']
        lab.email = request.POST['email']
        lab.phone = request.POST['phone']
        
        if 'pic' in request.FILES:
            lab.pic = request.FILES['lab_pic']
        lab.save()
        return render(request,'ledit.html',{'lab':lab,'msg':'Profile has been updated'})
    return render(request,'ledit.html',{'lab':lab})


def ldash(request):
    
    return render(request,'ldash.html')
def lchangepass(request):
    lab=Assistants.objects.get(email=request.session['email'])
    if request.method=='POST':
        if request.POST['opassword'] == lab.password:
            if request.POST['npassword'] == request.POST['rpassword']:
                lab.password= request.POST['npassword']
                return render(request,'lchangepass.html',{'msg':'password changed successfully','lab':lab})
            return render(request,'lchangepass.html',{'msg':'new passwords are not same','lab':lab})
        return render(request,'lchangepass.html',{'msg':'old password is incorrect','lab':lab})

    return render(request,'lchangepass.html',{'lab':lab})

def lforgot(request):
    
    if request.method=='POST':

        try:

            lab=Assistants.objects.get(email=request.POST['email'])
            if request.POST['email']==lab.email:
                fpass=lab.password
                subject='your password for login'
                message=f'Welcome to Life Care your password for login is: {fpass}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['email'], ]
                send_mail( subject, message, email_from, recipient_list )
                return render(request,'lforgot.html',{'msg':'password sent successfully'})        
        except:
            return render(request,'lforgot.html',{'msg':'invalid email'})
    return render(request,'lforgot.html')   