from django import forms

from job.models import Employer, JobApplication, JobSeekerProfile
from job.models.company import Company
from job.models.job_vacancy import JobVacancy
from job.models.location import Location


class JobVacancyForm(forms.ModelForm):
    city = forms.CharField(max_length=255)
    street = forms.CharField(max_length=255, required=False)
    building = forms.CharField(max_length=50, required=False)
    country = forms.CharField(max_length=255)
    postal_code = forms.CharField(max_length=20, required=False)
    salary = forms.DecimalField(max_digits=10, decimal_places=2)
    currency = forms.CharField(max_length=10, required=False)

    class Meta:
        model = JobVacancy
        fields = ['title', 'description', 'salary', 'currency']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class CompanyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Company
        fields = ['name', 'description', 'website', 'city', 'street', 'building', 'country', 'postal_code']

    name = forms.CharField(max_length=255, required=True, label='Назва компанії')
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False, label='Опис компанії')
    website = forms.URLField(required=False, label='Вебсайт компанії')

    city = forms.CharField(max_length=255, required=True, label='Місто')
    street = forms.CharField(max_length=255, required=False, label='Вулиця')
    building = forms.CharField(max_length=50, required=False, label='Будинок')
    country = forms.CharField(max_length=255, required=True, label='Країна')
    postal_code = forms.CharField(max_length=20, required=False, label='Поштовий код')

    def save(self, commit=True):
        location_data = {
            'city': self.cleaned_data['city'],
            'street': self.cleaned_data['street'],
            'building': self.cleaned_data['building'],
            'country': self.cleaned_data['country'],
            'postal_code': self.cleaned_data['postal_code']
        }

        location, created = Location.objects.get_or_create(**location_data)

        company = super().save(commit=False)
        company.location = location

        if commit:
            company.save()

            if self.user:
                try:
                    employer = self.user.employer_profile
                    employer.company = company
                    employer.save()
                except Employer.DoesNotExist:
                    pass

        return company


class JobSeekerProfileForm(forms.ModelForm):
    city = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'placeholder': 'City'}))
    street = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'placeholder': 'Street'}))
    building = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'placeholder': 'Building'}))
    country = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'placeholder': 'Country'}))
    postal_code = forms.CharField(max_length=20, required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'Postal Code'}))

    class Meta:
        model = JobSeekerProfile
        fields = ['skills', 'experience', 'education']
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your skills'}),
            'experience': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your experience'}),
            'education': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your education details'}),
        }

    def save(self, commit=True):
        location_data = {
            'city': self.cleaned_data.get('city'),
            'street': self.cleaned_data.get('street'),
            'building': self.cleaned_data.get('building'),
            'country': self.cleaned_data.get('country'),
            'postal_code': self.cleaned_data.get('postal_code')
        }

        if any(location_data.values()):
            location, created = Location.objects.get_or_create(**location_data)
            self.instance.location = location

        return super().save(commit)


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your cover letter'}),
        }


class ApplicationFilterForm(forms.Form):
    SORT_CHOICES = [
        ('date_asc', 'Дата подачі (старі до нових)'),
        ('date_desc', 'Дата подачі (нові до старих)'),
    ]
    sort_by = forms.ChoiceField(choices=SORT_CHOICES, required=False)
    has_cover_letter = forms.BooleanField(required=False, label='Має супровідний лист')
