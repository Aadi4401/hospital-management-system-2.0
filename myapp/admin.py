from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display=['id','fname','lname','email','password','phone','address','age','gender','pic']
@admin.register(Appointments)
class AdminAppointmentsUser(admin.ModelAdmin):
    list_display=['id','patient','doctor','date','time','pay_method','pay_id','amount','verify','pay_at']
