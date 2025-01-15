from django.db import models
from django.contrib.auth.models import User

##----------------------------------------------------------------------------------   word
class Word(models.Model):

    word = models.CharField(max_length=200, unique=True, verbose_name='Word')

    def __str__(self):
        return self.word

    class Meta:
        verbose_name = "Word"
        verbose_name_plural = "Words"
        ordering = ['word']

##----------------------------------------------------------------------------------   synonym

class Synonym(models.Model):

    synonym = models.CharField(max_length=200, verbose_name='Synonym')
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='synonyms', verbose_name='Associated Word')

    def __str__(self):
        return f"{self.synonym} (for {self.word.word})"

    class Meta:
        verbose_name = "Synonym"
        verbose_name_plural = "Synonyms"
        indexes = [
            models.Index(fields=['word', 'synonym']),
        ]

##----------------------------------------------------------------------------------   userprofile

from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=200, null=True, blank=True, verbose_name='First Name')
    last_name = models.CharField(max_length=200, null=True, blank=True, verbose_name='Last Name')
    email = models.EmailField(verbose_name='Email', unique=True)
    profile_image = models.ImageField(
        upload_to='uploads/profiles/',
        default='uploads/profiles/default-profile.png'
    )
    bio = models.TextField(null=True, blank=True, verbose_name='Biography', max_length=500)
    additional_info = models.CharField(max_length=255, null=True, blank=True, verbose_name='Additional Information')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        indexes = [
            models.Index(fields=['user']),
        ]


##----------------------------------------------------------------------------------   FavoriteWord


class FavoriteWord(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_words', verbose_name='User')
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='favorited_by', verbose_name='Word')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Added At')

    def __str__(self):
        return f"{self.word.word}"

    class Meta:
        verbose_name = "Favorite Word"
        verbose_name_plural = "Favorite Words"
        unique_together = ('user', 'word')
        ordering = ['-added_at']