from django.urls import path

from app import views

urlpatterns = [
    path('token/obtain/', views.get_token, name='get_token'),
    path('upload/', views.upload, name='upload'),
    path('tasks/<task_id>', views.get_status, name='get_status')
]
