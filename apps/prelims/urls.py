from django.urls import path

from . import views

app_name = 'prelims'

urlpatterns = [
    path('', views.question_list, name='list'),
    path('daily/', views.daily_question, name='daily'),
    path('<int:pk>/', views.question_practice, name='practice'),
    path('<int:pk>/submit/', views.submit_answer, name='submit_answer'),
]
