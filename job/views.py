from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django.views.generic.base import View
from django.views.generic.detail import DetailView

from job.forms import CompanyForm, JobVacancyForm
from job.models import Company
from job.models.job_vacancy import JobVacancy


class JobVacancyListView(LoginRequiredMixin, ListView):
    model = JobVacancy
    template_name = 'job_list.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        return JobVacancy.objects.filter(recruiter__user=self.request.user)


class JobVacancyCreateView(LoginRequiredMixin, CreateView):
    model = JobVacancy
    form_class = JobVacancyForm
    template_name = 'job_form.html'
    success_url = reverse_lazy('vacancy-list')

    def form_valid(self, form):
        form.instance.recruiter = self.request.user.recruiter_profile
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
        form = CompanyForm()
        return render(request, 'create_company.html', {'form': form})

    def post(self, request):
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('company_list')  # Redirect to company list or another page
        return render(request, 'create_company.html', {'form': form})


class CompanyDetailView(DetailView):
    model = Company
    template_name = 'company_detail.html'
    context_object_name = 'company'


class CompanyListView(ListView):
    model = Company
    template_name = 'company_list.html'  # шаблон для відображення списку компаній
    context_object_name = 'companies'
