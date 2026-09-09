from django.contrib import admin
from .models import Student
# Register your models here.
class StudentDetail(admin.ModelAdmin):
    list_display = ['id','name', 'roll_no', 'course', 'email']
admin.site.register(Student,StudentDetail)