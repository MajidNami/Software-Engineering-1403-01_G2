from django.db import models

# Create your models here.
from django.contrib.auth.models import User

# Model for storing common words

class PersianWord(models.Model):
    word = models.CharField(max_length=100, unique=True)
    frequency = models.IntegerField(default=0)  # Frequency of usage for ranking suggestions.

    def __str__(self):
        return self.word


# (Optional) Model for storing user-specific typing history
from django.contrib.auth.models import User
class UserHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(PersianWord, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)  # Tracks when the word was last used.
