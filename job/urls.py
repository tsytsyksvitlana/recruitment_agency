from django.urls import path

from job.views import (
    CompanyDetailView,
    CompanyListView,
    CreateCompanyView,
    JobApplicationCreateView,
    JobSeekerProfileCreateView,
    JobSeekerProfileDetailView,
    JobSeekerProfileUpdateView,
    JobVacancyCreateView,
    JobVacancyDetailView,
    JobVacancyListView,
    JobVacancyManagementListView,
    JobVacancyUpdateView,
    MyCompanyView,
    RecruiterListView,
    activate_vacancy,
    deactivate_vacancy
)

urlpatterns = [
    path('vacancies/manage/', JobVacancyManagementListView.as_view(), name='vacancy-list'),
    path('vacancy/create/', JobVacancyCreateView.as_view(), name='vacancy-create'),
    path('vacancy/<int:pk>', JobVacancyDetailView.as_view(), name='vacancy_detail'),
    path('<int:pk>/edit/', JobVacancyUpdateView.as_view(), name='vacancy-edit'),
    path('<int:pk>/deactivate/', deactivate_vacancy, name='vacancy-deactivate'),
    path('<int:pk>/activate/', activate_vacancy, name='vacancy-activate'),

    path('candidates/', JobVacancyUpdateView.as_view(), name='candidates-list'),

    path('jobseeker/vacancies/', JobVacancyListView.as_view(), name='jobseeker_job_vacancies_list'),
    path('jobseeker/apply/<int:vacancy_id>/', JobApplicationCreateView.as_view(), name='job_application_create'),


    path('profile/', JobSeekerProfileDetailView.as_view(), name='profile_view'),
    path('profile/edit/', JobSeekerProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/create/', JobSeekerProfileCreateView.as_view(), name='profile_create'),

    path('company/create/', CreateCompanyView.as_view(), name='create_company'),
    path('companies/', CompanyListView.as_view(), name='company_list'),
    path('company/<int:pk>/', CompanyDetailView.as_view(), name='company_detail'),
    path('my-company/', MyCompanyView.as_view(), name='my_company'),

    path('recruiters/', RecruiterListView.as_view(), name='recruiter_list'),
]
