from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
 
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='tracking/login.html'
    ), name='login'),

    path('accounts/logout/', auth_views.LogoutView.as_view(
        template_name='tracking/logout.html',
        next_page='/'
    ), name='logout'),


    path('', include('tracking.urls')),
]