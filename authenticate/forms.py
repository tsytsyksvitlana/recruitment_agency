from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from authenticate.models import User
from job.models import Company, Recruiter
from job.models.employer import Employer


class UserRegisterForm(UserCreationForm):
    """
    Form that allows to register as jobseeker or employer.
    """
    first_name = forms.CharField(max_length=150, required=True, label="First Name")
    last_name = forms.CharField(max_length=150, required=True, label="Last Name")

    role = forms.ChoiceField(
        choices=[("jobseeker", "Job Seeker"), ("employer", "Employer")],
        required=True,
        label="Select your role"
    )
    company_name = forms.CharField(
        max_length=255, required=False, label="Company Name"
    )

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password1", "password2", "role")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data["role"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        # Set username from email to avoid the duplicate key error
        user.username = self.cleaned_data["email"]

        if commit:
            user.save()

            if user.role == "employer":
                company_name = self.cleaned_data.get("company_name")
                if company_name:
                    company, created = Company.objects.get_or_create(name=company_name)
                    Employer.objects.create(user=user, company=company)

        return user


class UserLoginForm(AuthenticationForm):
    """
    Form for user authentication which allows users
    to log in using their email and password.
    """
    username = forms.EmailField(label="Email")  # Use email instead of username

    class Meta:
        model = User
        fields = ("username", "password")


class RecruiterCreateForm(forms.ModelForm):
    """
    Form for employer to create a recruiter.
    """
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True, label="Confirm Password")
    first_name = forms.CharField(max_length=150, required=True, label="First Name")
    last_name = forms.CharField(max_length=150, required=True, label="Last Name")

    class Meta:
        model = User
        fields = ("email", "password", "confirm_password", "first_name", "last_name")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, employer, commit=True):
        user = User(
            email=self.cleaned_data["email"],  # Use email instead of username
            first_name=self.cleaned_data["first_name"],  # Save first name
            last_name=self.cleaned_data["last_name"],  # Save last name
            role="recruiter",
            username=self.cleaned_data["email"]  # Assign email as username
        )
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            Recruiter.objects.create(user=user, company=employer.company)
        return user
