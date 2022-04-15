from django.contrib import admin

from Lab.models import Assistants

# Register your models here.
@admin.register(Assistants)
class AdminAssistants(admin.ModelAdmin):
    list_display=['id','name','email','password','phone','lab_pic']