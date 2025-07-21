from .views import Post,forms
from django.urls import path

urlpatterns=[
    path('post',Post,name='Post'),
    path('forms',forms,name='Forms')
]