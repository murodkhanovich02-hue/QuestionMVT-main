from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.username


class Question(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('elementary', 'Elementary'),
        ('pre-intermediate', 'Pre-Intermediate'),
        ('intermediate', 'Intermediate'),
        ('upper-intermediate', 'Upper-Intermediate'),
    ]

    text = models.CharField(max_length=255, verbose_name="Savol matni")
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default='beginner',
    )



class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        related_name='answers',
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=255, verbose_name="Javob matni")
    is_correct = models.BooleanField(default=False, verbose_name="To‘g‘ri javobmi?")

    def __str__(self):
        return f"{self.text} ({'To‘g‘ri' if self.is_correct else 'Noto‘g‘ri'})"
