from django.urls import path
from . import views

app_name = 'tracking'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('new-entry/', views.time_entry_create, name='time_entry_create'),
    path('entries/', views.time_entries_list, name='time_entries_list'),
]