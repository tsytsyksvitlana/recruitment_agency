import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django.views.generic.base import View
from django.views.generic.detail import DetailView

from job.forms import CompanyForm, JobVacancyForm
from job.models import Company, Employer, Recruiter
from job.models.job_vacancy import JobVacancy

logger = logging.getLogger(__name__)


class JobVacancyListView(LoginRequiredMixin, ListView):
    model = JobVacancy
    template_name = 'job_list.html'
    context_object_name = 'vacancies'

    # def get_queryset(self):
    #     user = self.request.user
    #     logger.debug(f"User {user.email} is requesting vacancies with role {user.role}")
    #
    #     if user.role == "employer":
    #         try:
    #             employer = Employer.objects.filter(user=user).first()
    #             employers = Employer.objects.filter(user=user).all()
    #             logger.debug(employers)
    #             return employers
    #             logger.debug(f"Employer found for user {user.email}, company: {employer.company.name}")
    #             vacancies = JobVacancy.objects.filter(company=employer.company)
    #             logger.debug(f"Found {vacancies.count()} vacancies for employer {employer.company.name}")
    #             return vacancies
    #         except Employer.DoesNotExist:
    #             logger.error(f"Employer profile does not exist for user {user.email}")
    #             return JobVacancy.objects.none()
    #
    #     elif user.role == "recruiter":
    #         try:
    #             recruiter = Recruiter.objects.filter(user=user).first()
    #             company = recruiter.company
    #             logger.debug(f"Recruiter found for user {user.email}, company: {company.name}")
    #
    #             # Вакансії рекрутера
    #             my_vacancies = JobVacancy.objects.filter(recruiter=recruiter)
    #             logger.debug(f"Found {my_vacancies.count()} vacancies for recruiter {user.email}")
    #
    #             # Вакансії колег
    #             colleagues_vacancies = JobVacancy.objects.filter(company=company).exclude(recruiter=recruiter)
    #             logger.debug(f"Found {colleagues_vacancies.count()} vacancies for recruiter colleagues in company {company.name}")
    #
    #             # Об'єднуємо вакансії рекрутера та колег
    #             all_vacancies = my_vacancies.union(colleagues_vacancies)
    #             logger.debug(f"Total vacancies for recruiter {user.email}: {all_vacancies.count()}")
    #             return all_vacancies
    #
    #         except Recruiter.DoesNotExist:
    #             logger.error(f"Recruiter profile does not exist for user {user.email}")
    #             return JobVacancy.objects.none()
    #
    #     logger.info(f"No valid role found for user {user.email}, returning empty queryset")
    #     return JobVacancy.objects.none()


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


def deactivate_vacancy(request, pk):
    vacancy = get_object_or_404(JobVacancy, pk=pk, recruiter__user=request.user)
    vacancy.is_active = False
    vacancy.save()
    return redirect('vacancy-list')


def activate_vacancy(request, pk):
    vacancy = get_object_or_404(JobVacancy, pk=pk, recruiter__user=request.user)
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
