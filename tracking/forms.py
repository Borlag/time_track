from django import forms
from .models import TimeEntry, Project

class TimeEntryForm(forms.ModelForm):
    class Meta:
        model = TimeEntry
        fields = ['project', 'hours', 'date', 'role']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'min': '0.5', 'max': '24'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'form-select'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'role': 'Роль в проекте',
            'hours': 'Часы работы',
            'date': 'Дата',
            'project': 'Проект',
            'description': 'Описание работы'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.filter(is_active=True)