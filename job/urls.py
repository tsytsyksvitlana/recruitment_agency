from django.urls import path

from job.views import (
    CompanyDetailView,
    CompanyListView,
    CreateCompanyView,
    JobVacancyCreateView,
    JobVacancyListView,
    JobVacancyUpdateView,
    deactivate_vacancy, activate_vacancy
)

urlpatterns = [
    path('vacancies', JobVacancyListView.as_view(), name='vacancy-list'),
    path('vacancy/create/', JobVacancyCreateView.as_view(), name='vacancy-create'),
    path('<int:pk>/edit/', JobVacancyUpdateView.as_view(), name='vacancy-edit'),
    path('<int:pk>/deactivate/', deactivate_vacancy, name='vacancy-deactivate'),
    path('<int:pk>/activate/', activate_vacancy, name='vacancy-activate'),

    path('candidates/', JobVacancyUpdateView.as_view(), name='candidates-list'),

    path('company/create/', CreateCompanyView.as_view(), name='create_company'),
    path('companies/', CompanyListView.as_view(), name='company_list'),
    path('company/<int:pk>/', CompanyDetailView.as_view(), name='company_detail'),
]
