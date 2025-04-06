from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from authenticate.models.user import User
from job.models.employer import Employer
from job.models.job_seeker import JobSeeker
from job.models.recruiter import Recruiter


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
        user.username = self.cleaned_data["email"]

        if commit:
            user.save()

            if user.role == "employer":
                if not Employer.objects.filter(user=user).exists():
                    Employer.objects.create(user=user, company=None)

            elif user.role == "jobseeker":
                if not JobSeeker.objects.filter(user=user).exists():
                    JobSeeker.objects.create(user=user)
        return user


class UserLoginForm(AuthenticationForm):
    """
    Form for user authentication which allows users
    to log in using their email and password.
    """
    username = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ("username", "password")


class RecruiterCreateForm(forms.ModelForm):
    """
    Form for employer to create a recruiter.
    """
    email = forms.EmailField(required=True, label="Email")
    password = forms.CharField(widget=forms.PasswordInput(), required=True, label="Password")
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
        email = cleaned_data.get("email")

        if password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match")

        if User.objects.filter(email=email).exists():
            self.add_error("email", "A user with this email already exists.")

        return cleaned_data

    def save(self, employer_user, commit=True):
        try:
            employer = employer_user.employer_profile
        except Employer.DoesNotExist:
            raise ValueError("Current user is not associated with an Employer profile.")

        user = User(
            email=self.cleaned_data["email"],
            username=self.cleaned_data["email"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            role="recruiter"
        )
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            Recruiter.objects.create(user=user, company=employer.company)
        return user
