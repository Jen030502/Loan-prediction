from django.contrib import admin
from django.urls import path
from home import views


urlpatterns = [
    path("", views.index, name='home'),
    path("signup", views.signupUser, name='signup'),
    path("login", views.loginUser, name='login'),
    path("logout", views.logoutUser, name='logout'),
    path("loanModel", views.loanModel, name='loanModel'),
    path('result',views.formInfo,name='result')
]
 