from django import forms
from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
        label="Username",
        max_length=100,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class' : 'form-control'
            }
        ),
        label="Password",
        max_length=255,
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                }
            ),
            'image': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control',
                }
            )
        }
        labels = {
            'content' : 'Content',
            'image' : 'Image'
        }


class GeneralPostForm(forms.ModelForm):
    choices = forms.ChoiceField(
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['choices'].choices = [ (forum.id, forum.title) for forum in Forum.objects.all() ]

class ForumForm(forms.Form):
    choices = forms.ChoiceField(
        label = "Switch Forum"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        list_var = [(0, "General")]
        list_var.extend([(forum.id, forum.title) for forum in Forum.objects.all()])
        self.fields['choices'].choices = list_var

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
