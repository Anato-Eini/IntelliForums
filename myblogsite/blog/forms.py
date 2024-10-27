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
                    'placeholder' : 'Enter your comment',
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
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class' : 'form-control'
            }
        ),
        label="Password",

    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class' : 'form-control'
            }
        ),
        label="Confirm Password"
    )
    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'picture']
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'image' : forms.ClearableFileInput(
                attrs={
                    'class' : 'button'
                }
            )
        }
        labels = {
            'username': 'Username',
            'picture': 'Profile Picture'
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords must match")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class SearchForm(forms.Form):
    content = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class' : 'form-control form-control-sm bg-gray-200 border-gray-200 shadow-none mb-4 mt-4',
                'placeholder' : 'Search forum',
            },
        ),
        label="",
    )
