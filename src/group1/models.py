from django.db import models
from django.contrib.auth.models import User


class PersianWord(models.Model):
    word = models.CharField(max_length=100, unique=True)
    frequency = models.IntegerField(default=0)

    class Meta:
        managed = False  
        db_table = 'group1_persianword'

    def __str__(self):
        return self.word

