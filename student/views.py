from django.forms.models import model_to_dict
from django.shortcuts import redirect, render
from .models import Student
from .forms import StudentForm
# Create your views here.
def display(request):
    stud=Student.objects.all()
    context={'stud':stud}
    print(context)
    
    return render(request,'display.html',context)

def insert(request):
    if request.method=='POST':
        form=StudentForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            
            
            Student.objects.create(
                name=form.cleaned_data['name'],
                roll_no=form.cleaned_data['roll_no'],
                image=form.cleaned_data.get('image'),
                course=form.cleaned_data['course'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
            )
            return redirect('display')
    else:
        form=StudentForm()
    #     name=request.POST.get('name')
    #     roll_no=request.POST.get('roll_no')
    #     image=request.FILES.get('image')
    #     course=request.POST.get('course')
    #     email=request.POST.get('email')
    #     address=request.POST.get('address')
    #     if name and roll_no and image and course and email and address:
        
    #         Student.objects.create(
    #             name=name,
    #             roll_no=roll_no,
    #             image=image,
    #             course=course,
    #             email=email,
    #             address=address,
    #         )
    #         return redirect('display')
    #     else:
    #         context['message']="All field are mandatory"
    # print(context)
    return render(request, 'insert.html', {'form': form})

def update(request,id):
    context={
        'operation':'update student'
    }
    try:

        student=Student.objects.get(id=id)
        context['student']=student
    except Student.DoesNotExist:
        context['error']='404 : Student Not Found!'
        return render(request, 'update.html', context)
    else:
        form=StudentForm(initial=model_to_dict(student))
    if request.method=='POST':
        form=StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student.name=form.cleaned_data['name']
            student.roll_no=form.cleaned_data['roll_no']
            if form.cleaned_data.get('image'):
                student.image=form.cleaned_data['image']
            student.course=form.cleaned_data['course']
            student.email=form.cleaned_data['email']
            student.address=form.cleaned_data['address']
            student.save()
    # if request.method=='POST':
    #     student.name=request.POST.get('name')
    #     student.roll_no=request.POST.get('roll_no')
    #     student.image=request.FILES.get('image')
    #     student.course=request.POST.get('course')
    #     student.address=request.POST.get('address')
    #     student.email=request.POST.get('email')
    #     context={
    #         'student':student
    #     }

    #     student.save()

            return redirect('display')
    context['form']=form
    return render(request,'update.html',context)
        

def delete(request,id):
    context={}
    
    try:
        student=Student.objects.get(id=id)
        context['student']=student
    except Student.DoesNotExist:
        context['error']='Student Not Found!'
    else:
        if request.method=='POST':
            student.delete()
            return redirect('display')

    return render(request,'delete.html',context)
