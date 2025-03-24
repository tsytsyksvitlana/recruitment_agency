from django import forms

from job.models.company import Company
from job.models.job_vacancy import JobVacancy
from job.models.location import Location


class JobVacancyForm(forms.ModelForm):
    class Meta:
        model = JobVacancy
        fields = ['title', 'description', 'company', 'location']


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'description', 'website', 'city', 'street', 'building', 'country', 'postal_code']

    name = forms.CharField(max_length=255, required=True, label='Назва компанії')
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False, label='Опис компанії')
    website = forms.URLField(required=False, label='Вебсайт компанії')

    # New fields for location
    city = forms.CharField(max_length=255, required=True, label='Місто')
    street = forms.CharField(max_length=255, required=False, label='Вулиця')
    building = forms.CharField(max_length=50, required=False, label='Будинок')
    country = forms.CharField(max_length=255, required=True, label='Країна')
    postal_code = forms.CharField(max_length=20, required=False, label='Поштовий код')

    # Override save method to create a Location and link it to the Company
    def save(self, commit=True):
        location_data = {
            'city': self.cleaned_data['city'],
            'street': self.cleaned_data['street'],
            'building': self.cleaned_data['building'],
            'country': self.cleaned_data['country'],
            'postal_code': self.cleaned_data['postal_code']
        }

        # Create or get location
        location, created = Location.objects.get_or_create(**location_data)

        # Create the company and link the location
        company = super().save(commit=False)
        company.location = location

        if commit:
            company.save()

        return company
