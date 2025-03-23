from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from authenticate.models import User


class UserRegisterForm(UserCreationForm):
    """
    Form for user registration which allows users to register by providing
    a username, email, password, and role (Recruiter or Job Seeker).
    """
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "role")

    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True, label="Select your role")


class UserLoginForm(AuthenticationForm):
    """
    Form for user authentication which allows users
    to log in using their email and password.
    """
    username = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ("username", "password")
