from django.contrib import admin
from django.urls import path, include
from .views import Register, Login, Admin, Adv, ADVBooking

urlpatterns = [
    path('user/register', Register.as_view()),
    path('user/login', Login.as_view()),
    path('admin/advisor', Admin.as_view()),
    path('user/<str:id>/advisor',Admin.as_view()),
    path('user/<str:id>/advisor/<int:a_id>',Adv.as_view()),
    path('user/<str:id>/advisor/booking',ADVBooking.as_view()),
]