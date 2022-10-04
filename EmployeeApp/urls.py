from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.login,name="login"),
    path('home',views.home,name="home"),
    path('addemp',views.addemployee,name="addemployee"),
    path('viewemp',views.viewemployee,name="viewemployee"),
    path('deleteemp/<int:id>',views.deleteemployee,name="deleteemployee"),
    path('assgproj',views.assignproject,name="assignproject"),
    path('projstat',views.projectstatus,name="projectstatus"),
    path('salstat',views.salarystatus,name="salarystatus"),
    path('empleave',views.employeeleave,name="employeeleave"),
    path('apprleave/<int:token>/<str:todo>',views.approveleave,name="approveleave"),
    path('profile',views.profile,name="profile"),
    path('myproj',views.myprojects,name="myprojects"),
    path('subproj/<int:pid>',views.submitproject,name="submitproject"),
    path('appleave',views.applyleave,name="applyleave"),
    path('logout',views.logout,name="logout"),
]
