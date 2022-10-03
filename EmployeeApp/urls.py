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
]
