# myproject/urls.py
from django.contrib import admin
from django.urls import path
from imagegen import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('accounts/login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.generate_image, name='generate_image'),
    path('create-session/', views.create_session, name='create_session'),
]
