import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django.views.generic.base import View
from django.views.generic.detail import DetailView

from job.forms import (
    CompanyForm,
    JobApplicationForm,
    JobSeekerProfileForm,
    JobVacancyForm
)
from job.models import (
    Company,
    Employer,
    JobApplication,
    JobSeekerProfile,
    Recruiter
)
from job.models.job_vacancy import JobVacancy

logger = logging.getLogger(__name__)


class JobVacancyManagementListView(LoginRequiredMixin, ListView):
    """
    View for managing job vacancies by employers and recruiters in certain company
    """
    model = JobVacancy
    template_name = 'job_list.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        user = self.request.user

        company = None

        if hasattr(user, 'employer_profile') and user.employer_profile.company:
            company = user.employer_profile.company
        elif hasattr(user, 'recruiter_profile') and user.recruiter_profile.company:
            company = user.recruiter_profile.company

        if not company:
            return JobVacancy.objects.none()

        return JobVacancy.objects.filter(company=company)


class JobVacancyCreateView(LoginRequiredMixin, CreateView):
    model = JobVacancy
    form_class = JobVacancyForm
    template_name = 'job_form.html'
    success_url = reverse_lazy('vacancy-list')

    def form_valid(self, form):
        try:
            form.instance.recruiter = self.request.user.recruiter_profile
        except ObjectDoesNotExist:
            messages.error(
                self.request, "Ваш профіль рекрутера не знайдено. Створіть профіль перед створенням вакансії."
            )
        return super().form_valid(form)


class JobVacancyUpdateView(LoginRequiredMixin, UpdateView):
    model = JobVacancy
    form_class = JobVacancyForm
    template_name = 'job_form.html'
    success_url = reverse_lazy('vacancy-list')


class JobVacancyDetailView(DetailView):
    model = JobVacancy
    template_name = 'job_detail.html'
    context_object_name = 'vacancy'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vacancy = self.get_object()
        applications = JobApplication.objects.filter(vacancy = vacancy).select_related()
        context['applications'] = applications
        return context


def deactivate_vacancy(request, pk):
    vacancy = get_object_or_404(JobVacancy, pk=pk)
    vacancy.is_active = False
    vacancy.save()
    return redirect('vacancy-list')


def activate_vacancy(request, pk):
    vacancy = get_object_or_404(JobVacancy, pk=pk)
    vacancy.is_active = True
    vacancy.save()
    return redirect('vacancy-list')


class CreateCompanyView(View):
    def get(self, request):
        form = CompanyForm(user=request.user)
        return render(request, 'create_company.html', {'form': form})

    def post(self, request):
        form = CompanyForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('my_company')
        return render(request, 'create_company.html', {'form': form})


class CompanyDetailView(DetailView):
    model = Company
    template_name = 'company_detail.html'
    context_object_name = 'company'


class MyCompanyView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        user = request.user
        try:
            employer_profile = user.employer_profile
            company = employer_profile.company

            if company is not None:
                return render(request, 'my_company.html', {'company': company})
            else:
                return render(request, 'my_company.html', {'company': None})

        except Employer.DoesNotExist:
            return render(request, 'my_company.html', {'company': None})


class CompanyListView(ListView):
    model = Company
    template_name = 'company_list.html'
    context_object_name = 'companies'


class RecruiterListView(LoginRequiredMixin, ListView):
    model = Recruiter
    template_name = "recruiter_list.html"
    context_object_name = 'recruiters'

    def get_queryset(self):
        if self.request.user.role != "employer":
            return redirect("login")

        employer = self.request.user.employer_profile
        company = employer.company

        return Recruiter.objects.filter(company=company)


class JobSeekerProfileCreateView(CreateView):
    model = JobSeekerProfile
    form_class = JobSeekerProfileForm
    template_name = 'profile_form.html'
    success_url = reverse_lazy('profile_view')

    def form_valid(self, form):
        form.instance.user = self.request.user.jobseeker_profile
        return super().form_valid(form)


class JobSeekerProfileUpdateView(UpdateView):
    model = JobSeekerProfile
    form_class = JobSeekerProfileForm
    template_name = 'profile_form.html'
    success_url = reverse_lazy('profile_view')

    def get_object(self, queryset=None):
        return self.request.user.jobseeker_profile.profile


class JobSeekerProfileDetailView(DetailView):
    model = JobSeekerProfile
    template_name = 'profile_view.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        try:
            profile = self.request.user.jobseeker_profile.profile
        except JobSeekerProfile.DoesNotExist:
            return None
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not context.get('profile'):
            context['create_profile_url'] = reverse('profile_create')
        return context


class JobVacancyListView(ListView):
    model = JobVacancy
    template_name = 'job_vacancies_list.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        queryset = JobVacancy.objects.all()

        search_title = self.request.GET.get('title', '')
        search_location = self.request.GET.get('location', '')

        if search_title:
            queryset = queryset.filter(title__icontains=search_title)

        if search_location:
            queryset = queryset.filter(location__icontains=search_location)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            jobseeker_profile = self.request.user.jobseeker_profile
            applied_vacancies = jobseeker_profile.applications.values_list('vacancy', flat=True)
            context['applied_vacancies'] = applied_vacancies

        return context


class JobApplicationCreateView(CreateView):
    model = JobApplication
    form_class = JobApplicationForm
    template_name = 'job_application_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancy'] = JobVacancy.objects.get(id=self.kwargs['vacancy_id'])
        return context

    def form_valid(self, form):
        form.instance.job_seeker = self.request.user.jobseeker_profile
        form.instance.vacancy = JobVacancy.objects.get(id=self.kwargs['vacancy_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('jobseeker_job_vacancies_list')
