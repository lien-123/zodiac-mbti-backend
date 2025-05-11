from django.db import models

# Create your models here.
# models.py
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mbti = models.CharField(max_length=4, choices=[
        ('INTJ', 'INTJ'), ('INTP', 'INTP'), ('ENTJ', 'ENTJ'), ('ENTP', 'ENTP'),
        ('INFJ', 'INFJ'), ('INFP', 'INFP'), ('ENFJ', 'ENFJ'), ('ENFP', 'ENFP'),
        ('ISTJ', 'ISTJ'), ('ISFJ', 'ISFJ'), ('ESTJ', 'ESTJ'), ('ESFJ', 'ESFJ'),
        ('ISTP', 'ISTP'), ('ISFP', 'ISFP'), ('ESTP', 'ESTP'), ('ESFP', 'ESFP')
    ], null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
