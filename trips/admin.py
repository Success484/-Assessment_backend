from django.contrib import admin
from .models import  Trip, DutyLog

# Register your models here.
admin.site.register(Trip)
admin.site.register(DutyLog)