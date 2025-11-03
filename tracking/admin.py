from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Project, TimeEntry

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'position', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'position')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'position')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'position'),
        }),
    )
    
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id_key', 'name', 'is_active', 'status', 'created_at')
    list_filter = ('is_active', 'status')
    search_fields = ('id_key', 'name')

@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'hours', 'date', 'created_at')
    list_filter = ('date', 'project')
    search_fields = ('user__username', 'project__name')