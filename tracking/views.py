from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import TimeEntry, Project
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
        form = TimeEntryForm(request.POST)
        if form.is_valid():
            time_entry = form.save(commit=False)
            time_entry.user = request.user
            time_entry.save()
            messages.success(request, 'Запись успешно добавлена!')
            return redirect('tracking:dashboard')
    else:
        form = TimeEntryForm(initial={'date': timezone.now().date()})
    
    return render(request, 'tracking/time_entry_form.html', {
        'form': form,
        'title': 'Новая запись времени'
    })

@login_required
def time_entries_list(request):
    entries = TimeEntry.objects.filter(user=request.user).order_by('-date')
    return render(request, 'tracking/time_entries.html', {
        'entries': entries
    })