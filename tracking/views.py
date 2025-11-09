from datetime import timedelta
from decimal import Decimal
from typing import Optional

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, models
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone

from .forms import TimeEntryForm
from .models import TimeEntry


def _format_hours(value: Optional[Decimal]) -> str:
    if value is None:
        return "0"
    normalized = value.normalize()
    text = format(normalized, 'f')
    return text.rstrip('0').rstrip('.') if '.' in text else text


@login_required
def dashboard(request):
    recent_entries = (
        TimeEntry.objects.filter(user=request.user)
        .select_related('project')
        .order_by('-date', '-created_at')[:10]
    )
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
            except IntegrityError as error:
                messages.error(request, f'Ошибка при сохранении записи: {error}')
            else:
                hours_display = _format_hours(time_entry.hours)
                if time_entry.is_overtime:
                    messages.success(request, f'Внесенные часы учтены в овертайм! +{hours_display} часов')
                else:
                    messages.success(request, f'Внесенные часы учтены в основное время! +{hours_display} часов')
                form = TimeEntryForm(user=request.user)
        else:
            messages.error(request, 'Форма заполнена некорректно.')
    else:
        form = TimeEntryForm(user=request.user)

    return render(request, 'tracking/time_entry_form.html', {
        'form': form,
        'title': 'Новая запись времени'
    })


@login_required
def time_entries_list(request):
    base_queryset = TimeEntry.objects.filter(user=request.user)
    entries = base_queryset.select_related('project').order_by('-date', '-created_at')[:10]

    week_ago = timezone.now().date() - timedelta(days=7)
    aggregates = base_queryset.aggregate(
        total_hours=models.Sum('hours'),
        regular_hours=models.Sum('hours', filter=Q(is_overtime=False)),
        overtime_hours=models.Sum('hours', filter=Q(is_overtime=True)),
        weekly_hours=models.Sum('hours', filter=Q(date__gte=week_ago)),
    )

    return render(request, 'tracking/time_entries.html', {
        'entries': entries,
        'total_hours': _format_hours(aggregates['total_hours']),
        'regular_hours': _format_hours(aggregates['regular_hours']),
        'overtime_hours': _format_hours(aggregates['overtime_hours']),
        'weekly_hours': _format_hours(aggregates['weekly_hours']),
    })
