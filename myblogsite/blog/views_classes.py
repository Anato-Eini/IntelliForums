from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView, LoginView
from django.shortcuts import render, redirect

class CustomAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def as_custom(self):
        return (
            f"<div class='form-group'>"
            f"<div class='username_label'>{self.fields['username'].label}</div>"
            f"{self['username']}</div>"
            f"<div class='form-group'>"
            f"<div class='password_label'>{self.fields['password'].label}</div>"
            f"{self['password']}</div>"
        )

class CustomLoginView(LoginView):
    """
    Custom Login View inherited from Django LoginView
    """

    template_name = 'login_form.html'
    form_class = CustomAuthenticationForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home', pk=0, page_number=1)
            else:
                form.add_error(None, "Invalid credentials")

        return render(request, self.template_name, {'form': form})


class CustomLogoutView(LogoutView):
    """
    Custom Logout View inherited from Django LogoutView
    """

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        response = super().dispatch(request, *args, **kwargs)
        return redirect('home', pk=0, page_number=1)