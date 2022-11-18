from django.urls import path
from . import views 


urlpatterns = [
    path('', views.home_page, name="home"),
    path('event/<str:pk>/', views.event_page, name="event"),
    path('registration-confirmation/<str:pk>/', views.registration_confirmation, name="registration-confirmation"),
    path('user/<str:pk>/', views.user_page, name="profile"),

    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name="register"),
    path('logout/', views.logout_request, name='logout'),

    path('account/', views.account_page, name="account"),
    path('project-submission/<str:pk>/', views.project_submission, name="project-submission"),
    path('update-submission/<str:pk>/', views.update_submission, name="update-submission"),
]