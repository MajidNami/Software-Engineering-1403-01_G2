from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'profile_image', 'bio', ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
