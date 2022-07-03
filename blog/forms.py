from django import forms

from .models import Post#, User

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        # fields = ('title', 'text', )
        fields = ['title', 'text', ]


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password',]
        widgets = {
            'password' : forms.PasswordInput()
        }
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
class LogInForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password',]
        widgets = {
            'password' : forms.PasswordInput()
        }
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
class ChangePassForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password',]
        widgets = {
            'password' : forms.PasswordInput()
        }
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user