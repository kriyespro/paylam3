from django.urls import path

from . import views

app_name = 'platform_admin'

urlpatterns = [
    path('', views.DashboardHome.as_view(), name='home'),

    path('backup/', views.BackupDownloadView.as_view(), name='backup_download'),
    path('restore/', views.RestoreUploadView.as_view(), name='restore_upload'),
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'),

    path('articles/', views.ArticleListView.as_view(), name='article_list'),
    path('articles/new/', views.ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', views.ArticleUpdateView.as_view(), name='article_update'),
    path('articles/<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),

    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/new/', views.PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),

    path('subjects/', views.SubjectListView.as_view(), name='subject_list'),
    path('subjects/<int:pk>/edit/', views.SubjectUpdateView.as_view(), name='subject_update'),

    path('questions/', views.QuestionListView.as_view(), name='question_list'),
    path('questions/new/', views.QuestionCreateView.as_view(), name='question_create'),
    path('questions/<int:pk>/edit/', views.QuestionUpdateView.as_view(), name='question_update'),
    path('questions/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='question_delete'),

    path('ncert-topics/', views.NcertTopicListView.as_view(), name='ncert_topic_list'),
    path('ncert-topics/new/', views.NcertTopicCreateView.as_view(), name='ncert_topic_create'),
    path('ncert-topics/<int:pk>/edit/', views.NcertTopicUpdateView.as_view(), name='ncert_topic_update'),
    path('ncert-topics/<int:pk>/delete/', views.NcertTopicDeleteView.as_view(), name='ncert_topic_delete'),

    path('ncert-questions/', views.NcertQuestionListView.as_view(), name='ncert_question_list'),
    path('ncert-questions/new/', views.NcertQuestionCreateView.as_view(), name='ncert_question_create'),
    path('ncert-questions/<int:pk>/edit/', views.NcertQuestionUpdateView.as_view(), name='ncert_question_update'),
    path('ncert-questions/<int:pk>/delete/', views.NcertQuestionDeleteView.as_view(), name='ncert_question_delete'),

    path('mains-questions/', views.MainsQuestionListView.as_view(), name='mains_question_list'),
    path('mains-questions/new/', views.MainsQuestionCreateView.as_view(), name='mains_question_create'),
    path('mains-questions/<int:pk>/edit/', views.MainsQuestionUpdateView.as_view(), name='mains_question_update'),
    path('mains-questions/<int:pk>/delete/', views.MainsQuestionDeleteView.as_view(), name='mains_question_delete'),

    path('users/', views.UserListView.as_view(), name='user_list'),
]
