from django.urls import path

from . import views

app_name = 'engagement'

urlpatterns = [
    path('', views.bookmark_list, name='bookmarks'),
    path('questions/<int:pk>/toggle/', views.toggle_bookmark, name='toggle_bookmark'),
]
