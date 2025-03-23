from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from authenticate.forms import UserLoginForm, UserRegisterForm


class UserRegisterView(CreateView):
    """
    View registers the user and redirects to the login page.
    """
    template_name = "register.html"
    success_url = reverse_lazy("login")
    form_class = UserRegisterForm


class UserLoginView(LoginView):
    """
    View logs in the user and redirects to the main page.
    """
    template_name = "login.html"
    form_class = UserLoginForm


class UserLogoutView(View):
    """
    View logs out the user and redirects to the login page.
    """
    def get(self, request):
        logout(request)
        return redirect("login")
