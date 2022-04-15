from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from random import randrange
from Doctor.models import Doctors
# Create your views here.
def index(request):
    return render(request,'index.html')

def register(request):
    if request.method == 'POST':

        try:
            User.objects.get(email=request.POST['email'])
            msg='email already registered'
            return render(request,'reg.html',{'msg':msg})        
        except:
            if request.POST['password']== request.POST['cpassword']:
                global temp
                temp={
                'fname':request.POST['fname'],
                'lname':request.POST['lname'],
                'email':request.POST['email'],
                'password':request.POST['password'],
                'phone':request.POST['phone'],    
                }
                otp = randrange(1111,9999)
                subject = 'welcome to Life Care'
                message = f'your otp for registeration is :  {otp}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['email'], ]
                send_mail( subject, message, email_from, recipient_list )
                return render(request,'otp.html',{'otp':otp})
            else:
                return render(request,'reg.html',{'msg':'both passwords are not same'}) 
    return render(request,'reg.html')



def otp(request):
    if request.method=='POST':
        if request.POST['otp'] == request.POST['uotp']:
            global temp
            User.objects.create(
            fname=temp['fname'],
            lname=temp['lname'],
            email=temp['email'],
            password=temp['password'],
            phone=temp['phone'],
            )
            return render(request,'reg.html',{'msg':'Account created successfully'})
        return render(request,'otp.html',{'msg':'invalid otp','otp':request.POST['otp']})
    return render(request,'reg.html')




def plogin(request):
    try:
        uid = User.objects.get(email=request.session['email'])
        return render(request,'pdash.html',{'uid':uid})
    except:
        if request.method == 'POST':
            # try:
                uid = User.objects.get(email=request.POST['email'])
                if request.POST['password'] == uid.password:
                    request.session['email'] = request.POST['email']
                    return render(request,'pdash.html',{'uid':uid})
                return render(request,'plogin.html',{'msg':'Inncorrect password','uid':uid})
            # except:
            #     msg = 'Email is not register'
            #     return render(request,'plogin.html',{'msg':msg,'uid':uid})
        return render(request,'plogin.html')

def plogout(request):
    del request.session['email']
    return render(request,'plogin.html') 



def pedit(request):
    uid = User.objects.get(email=request.session['email'])
    if request.method == 'POST':
        uid.fname = request.POST['fname']
        uid.lname = request.POST['lname']
        uid.email = request.POST['email']
        uid.phone = request.POST['phone']
        uid.address = request.POST['address']
        uid.age = request.POST['age']
        uid.gender = request.POST['gender']
        
        if 'pic' in request.FILES:
            uid.pic = request.FILES['pic']
        uid.save()
        return render(request,'pedit.html',{'uid':uid,'msg':'Profile has been updated'})
    return render(request,'pedit.html',{'uid':uid}) 
     

def pforgot(request):
    
    if request.method=='POST':

        try:

            uid=User.objects.get(email=request.POST['email'])
            if request.POST['email']==uid.email:
                fpass=uid.password
                subject='your password for login'
                message=f'Welcome to Life Care your password for login is: {fpass}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['email'], ]
                send_mail( subject, message, email_from, recipient_list )
                return render(request,'pforgot.html',{'msg':'password sent successfully'})        
        except:
            return render(request,'pforgot.html',{'msg':'invalid email'})
    return render(request,'pforgot.html')   



def pchangepass(request):
    uid=User.objects.get(email=request.session['email'])
    if request.method=='POST':
        if request.POST['opassword'] == uid.password:
            if request.POST['npassword'] == request.POST['rpassword']:
                uid.password= request.POST['npassword']
                uid.save()
                return render(request,'pchangepass.html',{'msg':'password changed successfully','uid':uid})
            return render(request,'pchangepass.html',{'msg':'new passwords does not match','uid':uid})
        return render(request,'pchangepass.html',{'msg':'old password is incorrect','uid':uid})
    return render(request,'pchangepass.html',{'uid':uid})

def cancer(request):
    return render(request,'cancer.html')
def organ(request):
    return render(request,'organ.html')
def covid(request):
    return render(request,'covid.html')
def generic(request):
    return render(request,'generic.html')
def services(request):
    return render(request,'services.html')
def contact(request):
    return render(request,'contact.html')
def about(request):
    return render(request,'about.html')
def pdash(request):
    return render(request,'pdash.html')
def dashboard(request):
    return render(request,'dashboard.html')

#json javascript jquesry
def getspe(request):
    data = list(Doctors.objects.filter(specialization=request.GET['value']).values())
    return JsonResponse({'data':data})

def appointment(request):
    uid=User.objects.get(email=request.session['email'])
    doctor=Doctors.objects.all() 
    if request.method=='POST':
        doctor = Doctors.objects.get(id=request.POST['doctorname'])
        Appointments.objects.create(
            doctor = doctor,
            pay_method = request.POST['pay_method'],
            date = request.POST['date'],
            time = request.POST['time'],
            patient = uid,
            amount = doctor.fees
    )
        return render(request,'appointment.html',{'msg':'appointment booked successfully','uid':uid})
    return render(request,'appointment.html',{'uid':uid,'doctor':doctor})