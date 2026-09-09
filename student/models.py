from django.db import models

# Create your models here.
class Student(models.Model):
    COURSES=[
        ('PFS','Python Full Stack'),
        ('JFS','Java Full Stack'),
        ('MERN','MERN Stack'),
    ]
    name=models.CharField(max_length=100)
    image=models.ImageField(blank=True)
    roll_no=models.IntegerField()
    address=models.TextField()
    course=models.CharField(max_length=100,choices=COURSES,null=True)
    email=models.EmailField(null=True)

    def __str__(self):
        return self.name