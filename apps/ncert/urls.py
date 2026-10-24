from django.urls import path

from . import views

app_name = 'ncert'

urlpatterns = [
    path('', views.question_list, name='list'),
    path('topics/', views.topic_options, name='topic_options'),
    path('<int:pk>/', views.question_practice, name='practice'),
    path('<int:pk>/submit/', views.submit_answer, name='submit_answer'),
]
