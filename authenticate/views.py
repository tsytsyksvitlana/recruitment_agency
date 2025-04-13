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
from logs.models.action_log import ActionLog


class UserRegisterView(CreateView):
    """
    View registers the user and redirects to the login page.
    """
    template_name = "register.html"
    success_url = reverse_lazy("login")
    form_class = UserRegisterForm

    def form_valid(self, form):
        response = super().form_valid(form)
        ActionLog.objects.create(user=self.object, action="User registered")
        return response


class UserLoginView(LoginView):
    """
    View logs in the user and redirects to the main page.
    """
    template_name = "login.html"
    form_class = UserLoginForm

    def form_valid(self, form):
        ActionLog.objects.create(user=form.get_user(), action="User logged in")
        return super().form_valid(form)


class UserLogoutView(View):
    """
    View logs out the user and redirects to the login page.
    """
    def get(self, request):
        ActionLog.objects.create(user=request.user, action="User logged out")
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

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != "employer":
            return redirect("login")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = RecruiterCreateForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = RecruiterCreateForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            ActionLog.objects.create(
                user=request.user,
                action=f"Recruiter account created for {form.cleaned_data['email']}"
            )
            return redirect("index")
        return render(request, self.template_name, {"form": form})
