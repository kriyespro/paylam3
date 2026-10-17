from django.urls import path

from . import views

app_name = 'evaluations'

urlpatterns = [
    path('', views.my_evaluations, name='list'),
    path('submit/<int:question_id>/', views.submission_create, name='submit'),
    path('<int:pk>/', views.submission_detail, name='detail'),
    path('<int:pk>/evaluate/', views.evaluation_create, name='evaluate'),
]
