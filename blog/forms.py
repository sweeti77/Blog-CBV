from django import forms
from .models import Blog, Category, Profile

from django.contrib.auth.models import User


class BlogForm(forms.ModelForm):
    # category = forms.widgets.CheckboxSelectMultiple()
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )



    class Meta:
        model = Blog
        exclude = ['slug', 'posted_date', 'updated_date', 'author',]



# updates username/email
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']

# update profile picture
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
