from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from authenticate.forms import (
    RecruiterCreateForm,
    UserLoginForm,
    UserRegisterForm
)


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


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        return render(request, 'index.html', {'user': user})


class RecruiterCreateView(LoginRequiredMixin, View):
    """
    View allows an employer to create a recruiter account.
    """
    template_name = "create_recruiter.html"

    def get(self, request):
        if request.user.role != "employer":
            return redirect("login")

        form = RecruiterCreateForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        if request.user.role != "employer":
            return redirect("login")

        form = RecruiterCreateForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return redirect("index")

        return render(request, self.template_name, {"form": form})
