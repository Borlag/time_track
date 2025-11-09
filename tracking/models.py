from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class CustomUser(AbstractUser):
    """Модель пользователя, определяет любого пользователя системы"""
    position = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"


class Project(models.Model):
    """Модель проекта"""
    id_key = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.id_key} - {self.name}"


class TimeEntry(models.Model):
    """Модель уникальной записи. Определяет связь проекта и пользоватял 
    с внесенной записью времени
    """
    ROLE_CHOICES = [
        ('executor', 'Исполнитель'),
        ('reviewer', 'Проверяющий'),
        ('consultant', 'Консультация'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('0.25')),
            MaxValueValidator(Decimal('24')),
        ],
    )
    date = models.DateField()
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='executor'
    )
    is_overtime = models.BooleanField(
        default=False,
        verbose_name='Овертайм',
        help_text='Овертайм'
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta: 
        unique_together = ['user', 'project', 'date', 'hours']
        verbose_name_plural = "Time_entries"
        ordering = ['-date', '-created_at']

    
    def __str__(self):
        return f"{self.user} - {self.project} - {self.hours}h - {self.date}"
    
