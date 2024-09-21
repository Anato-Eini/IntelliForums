from django import forms
from .models import *

class LoginForm(forms.Form):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class' :'form-control'
                }
            ),
            'password': forms.PasswordInput(
                attrs={
                    'class' :'form-control'
                }
            )
        }
        labels = {
            'username': 'Username',
            'password': 'Password'
        }


class GeneralPostForm(forms.Form):

    choices = forms.ChoiceField(
        choices=[ (forum.id, forum.title) for forum in Forum.objects.all() ],
        label="Upload to:"
    )
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class' : 'form-control'
                }
            ),
            'content': forms.Textarea(
                attrs={
                    'class' : 'form-control'
                }
            ),
            'image': forms.ClearableFileInput(
                attrs={
                    'class' : 'form-control'
                }
            )
        }
        labels = {
            'title': 'Title',
            'content': 'Content',
            'image': 'Image'
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class' :'form-control'
                }
            ),
            'content': forms.Textarea(
                attrs={
                    'class' : 'form-control'
                }
            ),
            'image' : forms.ClearableFileInput(
                attrs={
                    'class' : 'form-control'
                }
            )
        }
        labels = {
            'title' : 'Title',
            'content' : 'Content',
            'image' : 'Upload an Image'
        }

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'birth_date']
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class' : 'form-control'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class' : 'form-control'
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'password': forms.PasswordInput(
                attrs={
                    'class' : 'form-control'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control'
                },
            ),
            'birth_date': forms.DateField(),
        }
        labels = {
            'username': 'Username',
            'password': 'Password',
            'email': 'Email',
            'birth_date': 'Birth date',
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }
