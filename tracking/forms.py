from django.core.exceptions import ValidationError
from django.utils import timezone
from django import forms
from django.db import models

from .models import TimeEntry, Project


class TimeEntryForm(forms.ModelForm):
    class Meta:
        model = TimeEntry
        fields = ['project', 'role', 'hours', 'date', 'is_overtime', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hours': forms.NumberInput(attrs={
                'class': 'form-control', 
                'step': '0.5',
                'min': '0.5',
                'max': '24'
            }),
            'description': forms.Textarea(attrs={
                'rows': 3, 
                'class': 'form-control',
                'placeholder': 'Опишите выполненную работу...'
            }),
            'project': forms.Select(attrs={'class': 'form-select'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'is_overtime': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'role': 'Ваша роль',
            'hours': 'Затраченное время (часы)',
            'date': 'Дата работы',
            'project': 'Проект',
            'is_overtime': 'Это овертайм?',
            'description': 'Описание работы'
        }
        help_texts = {
            'is_overtime': 'Отметьте если работали сверхурочно',
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.filter(is_active=True)
        
        self.fields['date'].initial = timezone.now().date()
    
    def clean(self):
        cleaned_data = super().clean()
        hours = cleaned_data.get('hours')
        date = cleaned_data.get('date')
        is_overtime = cleaned_data.get('is_overtime')
        
        if hours and date and self.user:
            if not is_overtime:
                total_hours_today = TimeEntry.objects.filter(
                    user=self.user,
                    date=date,
                    is_overtime=False
                ).exclude(pk=self.instance.pk if self.instance else None).aggregate(
                    total=models.Sum('hours')
                )['total'] or 0
                
                total_after_add = total_hours_today + hours
                
                if total_after_add > 8:
                    remaining_hours = 8 - total_hours_today
                    if remaining_hours > 0:
                        raise ValidationError(
                            f"Превышен лимит 8 часов в день!"
                            f"У вас уже {total_hours_today} часов за {date}. "
                            f"Доступно еще {remaining_hours} часов. "
                            f"или ставьте время в овертайм"
                        )
                    else:
                        raise ValidationError(
                            f"Вы уже отработали 8 часов за {date}. "
                            f"Отметьте 'Это овертайм?' чтобы добавить сверхурочные часы."
                        )
        
        return cleaned_data
    
    def clean_hours(self):
        hours = self.cleaned_data.get('hours')
        if hours and hours <= 0:
            raise ValidationError("Часы должны быть больше 0")
        if hours and hours > 24:
            raise ValidationError("Нельзя указать больше 24 часов за день")
        return hours