from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import student,course,Tutor
from django.contrib.auth.decorators import login_required
import os
# Create your views here.
def home(request):
    return render(request,'home.html')

def signup(request):
    return render(request,'signup.html')

def loginpage(request):
    return render(request,'login.html')        

def about(request):
    return render(request,'about.html')    

def welcome(request):
    if 'uid' in request.session:
        return render(request,'welcome.html')    
    return redirect('login')

@login_required(login_url='login')
def tutorhome(request):
    if 'uid' in request.session:
        return render(request,'tutorhome.html')
    return redirect('login')

@login_required(login_url='login')
def course1(request):
    uid = course.objects.get(id=request.session["uid"])
    return render(request,'course.html',{'uid':uid})    

@login_required(login_url='login')
def student1(request):
    courses=course.objects.all()
    context={'courses':courses}
    return render(request,'student.html',context) 

#......Msg Passing and Check Username and Password....
def usercreate(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        password=request.POST['password']
        cpassword=request.POST['cpassword']
        email=request.POST['email']
        user_address=request.POST['user_address']
        user_gender=request.POST['user_gender']
        user_mobile=request.POST['user_mobile']

        if request.FILES.get('user_photo') is not None:
            user_photo=request.FILES['user_photo']
        else:
            user_photo="/static/image/default.png"
        if password==cpassword:  #  password matching......
            if User.objects.filter(username=username).exists(): #check Username Already Exists..
                messages.info(request, 'This username already exists!!!!!!')
                print("Username already Taken..")
                return redirect('signup')
        
            else:
                user=User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
                user.save()
                #sel1 = request.POST['sel']
        
                u=User.objects.get(id=user.id)
                user1=Tutor(user_address=user_address,user_gender=user_gender,user=u,user_mobile=user_mobile,user_photo=user_photo)
                user1.save()
                
                return redirect('loginpage')
            return render(request,'signup.html')   
        else:
            messages.info(request, 'Password doesnt match!!!!!!!')
            print("Password is not Matching.. ") 
            return redirect('signup')   
        return redirect('login')
    
    return render(request,'signup.html')
#User login functionality view
def login(request): 
    
        if request.method == 'POST':
            try:
                username = request.POST['username']
                password = request.POST['password']
                user = auth.authenticate(username=username, password=password)
                request.session["uid"] = user.id
                if user is not None:
                    if user.is_staff:
                        auth.login(request,user)
                        messages.info(request, f'Welcome {username}')
                        return redirect('welcome')
                    else:
                        
                        auth.login(request,user)
                        messages.info(request,f'Welcome {username}')
                        return redirect('tutorhome')
            
                else:
                    messages.info(request, 'Invalid username or password')
                    return redirect('loginpage')
            except:
                messages.info(request,'invalid login')
        return render(request,'login.html')   
    
#User logout functionality view
def logout(request):
    request.session["uid"] = ""
    auth.logout(request)
    return redirect('home')

@login_required(login_url='login')
def add_course(request):
    if request.method=='POST':
        cors=request.POST['course']
        cfee=request.POST['cfee']
        print(cors)
        crs=course()
        crs.course_name=cors
        crs.fee=cfee
        crs.save()
        print("hii")
        return redirect('student1')

@login_required(login_url='login')
def add_student(request):
    if request.method=='POST':
        # adno=request.POST['adno']
        sname=request.POST['sname']
        address=request.POST['address']
        age=request.POST['age']
        jdate=request.POST['jdate']
        sel1 = request.POST['sel']
        course1=course.objects.get(id=sel1)
        std=student(std_name=sname,
                    std_address=address,
                    std_age=age,
                    Join_date=jdate,
                    course=course1)
        std.save()
        print("hii")
        return redirect('show_student_details')

@login_required(login_url='login')
def show_student_details(request):
    std=student.objects.all()
    return render(request,'show_students.html',{'std':std})

@login_required(login_url='login')
def delete_students(request,pk):
    std=student.objects.get(id=pk)
    std.delete()
    return redirect('show_student_details')

@login_required(login_url='login')
def show_tutors(request):
    user=Tutor.objects.all()
    return render(request,'show_tutors.html',{'user':user})

@login_required(login_url='login')
def delete_tutors(request,pk):
    user=User.objects.get(id=pk)
    user.delete()
    return redirect('show_tutors')

@login_required(login_url='login')
def edittutor(request):
    if request.method=='POST':
        umember=Tutor.objects.get(user=request.user)
        umember.user.first_name=request.POST.get('first_name')
        umember.user.last_name=request.POST.get('last_name')
        umember.user.username=request.POST.get('username')
        umember.user.email=request.POST.get('email')
        umember.user_address=request.POST.get('user_address')
        umember.user_mobile=request.POST.get('user_mobile')
        if request.FILES.get('user_photo') is not None:
            if not umember.user_photo=="/static/image/default.png":
                os.remove(umember.user_photo.path)
                umember.user_photo=request.FILES['user_photo']
            else:
                umember.user_photo=request.FILES['user_photo']
        else:
            os.remove(umember.user_photo.path)
            umember.user_photo="/static/image/default.png"
        umember.user.save()
        umember.save()
        return redirect('tutorprofile')
    umember=Tutor.objects.get(user=request.user)
    context={'umember':umember}
    return render(request,'edittutor.html',context)  

@login_required(login_url='login')
def tutorprofile(request):
    user=Tutor.objects.filter(user=request.user)
    context={'user':user}
    return render(request,'tutorprofile.html',context)

@login_required(login_url='login')
#Load Edit Page....
def editpage(request,pk):
    students=student.objects.get(id=pk)
    return render(request,'profile.html',{'students':students})

#Editing..
@login_required(login_url='login')
def edit_student_details(request,pk):
    if request.method=='POST':
        students = student.objects.get(id=pk)
        students.std_name = request.POST.get('std_name')
        students.std_address = request.POST.get('std_address')
        students.std_age = request.POST.get('std_age')
        students.Join_date = request.POST.get('Join_date')
        students.save()
        return redirect('show_student_details')
    return render(request, 'profile.html')




