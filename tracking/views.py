from datetime import timedelta

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import models

from .models import TimeEntry
from .forms import TimeEntryForm


@login_required
def dashboard(request):
    recent_entries = TimeEntry.objects.filter(user=request.user)[:10]
    return render(request, 'tracking/dashboard.html', {
        'recent_entries': recent_entries
    })

@login_required
def time_entry_create(request):
    if request.method == 'POST':
        form = TimeEntryForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                time_entry = form.save(commit=False)
                time_entry.user = request.user
                time_entry.save()
                
                if time_entry.is_overtime:
                    messages.success(request, f'Внесенные часы учтены в овертайм! +{time_entry.hours} часов')
                else:
                    messages.success(request, f'Внесенные часы учтены в основное время! +{time_entry.hours} часов')
                
                form = TimeEntryForm(user=request.user)
                
            except Exception as e:
                messages.error(request, f'Ошибка при сохранении: {e}')
        else:
            messages.error(request, 'Форма заполнена не корректно.')
    else:
        form = TimeEntryForm(user=request.user)
    
    return render(request, 'tracking/time_entry_form.html', {
        'form': form,
        'title': 'Новая запись времени'
    })


@login_required
def time_entries_list(request):
    entries = TimeEntry.objects.filter(user=request.user).order_by('-date', '-created_at')[:10]
    
    total_hours = TimeEntry.objects.filter(user=request.user).aggregate(
        total=models.Sum('hours')
    )['total'] or 0
    
    regular_hours = TimeEntry.objects.filter(
        user=request.user, 
        is_overtime=False
    ).aggregate(total=models.Sum('hours'))['total'] or 0
    
    overtime_hours = TimeEntry.objects.filter(
        user=request.user, 
        is_overtime=True
    ).aggregate(total=models.Sum('hours'))['total'] or 0
    
    week_ago = timezone.now().date() - timedelta(days=7)
    weekly_hours = TimeEntry.objects.filter(
        user=request.user,
        date__gte=week_ago
    ).aggregate(total=models.Sum('hours'))['total'] or 0
    
    return render(request, 'tracking/time_entries.html', {
        'entries': entries,
        'total_hours': total_hours,
        'regular_hours': regular_hours,
        'overtime_hours': overtime_hours,
        'weekly_hours': weekly_hours,
    })