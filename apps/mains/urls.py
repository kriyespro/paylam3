from django.urls import path

from . import views

app_name = 'mains'

urlpatterns = [
    path('', views.question_list, name='list'),
    path('daily/', views.daily_question, name='daily'),
    path('<int:pk>/', views.question_practice, name='practice'),
]
