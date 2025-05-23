import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django.views.generic.base import View
from django.views.generic.detail import DetailView

from job.forms import (
    ApplicationFilterForm,
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
    Location,
    Recruiter
)
from job.models.job_vacancy import JobVacancy
from logs.models.action_log import ActionLog

logger = logging.getLogger(__name__)


def log_action(user, action_type, description):
    ActionLog.objects.create(user=user, action=action_type, description=description)


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
        user = self.request.user

        location_data = {
            "city": form.cleaned_data.get("city"),
            "street": form.cleaned_data.get("street"),
            "building": form.cleaned_data.get("building"),
            "country": form.cleaned_data.get("country"),
            "postal_code": form.cleaned_data.get("postal_code"),
        }

        location, created = Location.objects.get_or_create(**location_data)
        form.instance.location = location

        try:
            if hasattr(user, 'recruiter_profile'):
                recruiter = user.recruiter_profile
                form.instance.recruiter = recruiter
                form.instance.company = recruiter.company
            elif hasattr(user, 'employer_profile'):
                employer = user.employer_profile
                form.instance.recruiter = None
                form.instance.company = employer.company
            else:
                raise ObjectDoesNotExist("Профіль не знайдено")
        except ObjectDoesNotExist:
            messages.error(
                self.request, "Ваш профіль не знайдено. Створіть профіль перед створенням вакансії."
            )
            return self.form_invalid(form)

        response = super().form_valid(form)
        log_action(user, "create_vacancy", f"Created vacancy: {form.instance.title}")
        return response


class JobVacancyUpdateView(LoginRequiredMixin, UpdateView):
    model = JobVacancy
    form_class = JobVacancyForm
    template_name = 'job_form.html'
    success_url = reverse_lazy('vacancy-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_action(self.request.user, "update_vacancy", f"Updated vacancy: {form.instance.title}")
        return response


class JobVacancyDetailView(DetailView):
    model = JobVacancy
    template_name = 'job_detail.html'
    context_object_name = 'vacancy'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vacancy = self.get_object()

        form = ApplicationFilterForm(self.request.GET)

        applications = JobApplication.objects.filter(vacancy=vacancy).select_related('job_seeker')

        if form.is_valid():
            sort_by = form.cleaned_data.get('sort_by')
            has_cover_letter = form.cleaned_data.get('has_cover_letter')

            if has_cover_letter is not None:
                if has_cover_letter:
                    applications = applications.exclude(cover_letter__exact='')
                else:
                    applications = applications.filter(cover_letter__exact='')

            if sort_by == 'date_asc':
                applications = applications.order_by('applied_at')
            elif sort_by == 'date_desc':
                applications = applications.order_by('-applied_at')

        context['applications'] = applications
        context['form'] = form
        return context


def deactivate_vacancy(request, pk):
    vacancy = get_object_or_404(JobVacancy, pk=pk)
    vacancy.is_active = False
    vacancy.save()
    log_action(request.user, "deactivate_vacancy", f"Deactivated vacancy: {vacancy.title}")
    return redirect('vacancy-list')


def activate_vacancy(request, pk):
    vacancy = get_object_or_404(JobVacancy, pk=pk)
    vacancy.is_active = True
    vacancy.save()
    log_action(request.user, "activate_vacancy", f"Activated vacancy: {vacancy.title}")
    return redirect('vacancy-list')


class CreateCompanyView(View):
    def get(self, request):
        form = CompanyForm(user=request.user)
        return render(request, 'create_company.html', {'form': form})

    def post(self, request):
        form = CompanyForm(request.POST, user=request.user)
        if form.is_valid():
            company = form.save()
            log_action(request.user, "create_company", f"Created company: {company.name}")
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
        response = super().form_valid(form)
        log_action(self.request.user, "create_profile", "Created job seeker profile")
        return response


class JobSeekerProfileUpdateView(UpdateView):
    model = JobSeekerProfile
    form_class = JobSeekerProfileForm
    template_name = 'profile_form.html'
    success_url = reverse_lazy('profile_view')

    def get_object(self, queryset=None):
        return self.request.user.jobseeker_profile.profile

    def form_valid(self, form):
        response = super().form_valid(form)
        log_action(self.request.user, "update_profile", "Updated job seeker profile")
        return response


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


class JobSeekerListView(LoginRequiredMixin, ListView):
    model = JobSeekerProfile
    template_name = 'job_seeker_list.html'
    context_object_name = 'job_seekers'

    def get_queryset(self):
        queryset = JobSeekerProfile.objects.all()
        search_name = self.request.GET.get('name', '')
        if search_name:
            queryset = queryset.filter(user__user__first_name__icontains=search_name)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_name'] = self.request.GET.get('name', '')
        return context


class JobVacancyListView(ListView):
    model = JobVacancy
    template_name = 'job_vacancies_list.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        queryset = JobVacancy.objects.all()

        search_title = self.request.GET.get('title', '')
        search_location = self.request.GET.get('location', '')
        sort_by = self.request.GET.get('sort', '')

        if search_title:
            queryset = queryset.filter(title__icontains=search_title)

        if search_location:
            queryset = queryset.filter(location__icontains=search_location)

        if sort_by == 'salary_asc':
            queryset = queryset.order_by('salary')
        elif sort_by == 'salary_desc':
            queryset = queryset.order_by('-salary')
        elif sort_by == 'newest':
            queryset = queryset.order_by('-created_at')
        elif sort_by == 'reviews':
            queryset = queryset.annotate(num_reviews=Count('reviews')).order_by('-num_reviews')
        elif sort_by == 'not_applied':
            if self.request.user.is_authenticated:
                jobseeker_profile = self.request.user.jobseeker_profile
                applied_vacancies = jobseeker_profile.applications.values_list('vacancy', flat=True)
                queryset = queryset.exclude(id__in=applied_vacancies)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            jobseeker_profile = self.request.user.jobseeker_profile
            applied_vacancies = jobseeker_profile.applications.values_list('vacancy', flat=True)
            context['applied_vacancies'] = applied_vacancies

        context['sort'] = self.request.GET.get('sort', '')
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
        response = super().form_valid(form)
        log_action(
            self.request.user,
            "apply_job",
            f"Applied to vacancy: {form.instance.vacancy.title}"
        )
        return response

    def get_success_url(self):
        return reverse_lazy('jobseeker_job_vacancies_list')
