from unicodedata import name
from django import views
from django.urls import include, path
from.import views

urlpatterns = [
    path('',views.home,name='home'),
    path('signup/',views.signup,name='signup'),
    path('loginpage/',views.loginpage,name='loginpage'),
    path('about/',views.about,name='about'),
    path('welcome/',views.welcome,name='welcome'),
    path('course1/',views.course1,name='course1'),
    path('student1/',views.student1,name='student1'),
    path('usercreate/',views.usercreate,name="usercreate"),
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name="logout"),
    path('add_student/',views.add_student,name="add_student"),
    path('add_course/',views.add_course,name="add_course"),
    path('show_student_details/',views.show_student_details,name="show_student_details"),
    path('show_tutors/',views.show_tutors,name='show_tutors'),
    path('delete_tutors/<int:pk>',views.delete_tutors,name='delete_tutors'),
    path('delete_students/<int:pk>',views.delete_students,name='delete_students'),
    path('tutorhome/',views.tutorhome,name='tutorhome'),
    path('edittutor/',views.edittutor,name='edittutor'),
    path('tutorprofile/',views.tutorprofile,name='tutorprofile'),
    path('edit_student_details/<int:pk>',views.edit_student_details,name='edit_student_details'),
    path('editpage/<int:pk>',views.editpage,name='editpage')

    ]

    
