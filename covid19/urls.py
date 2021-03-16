from django.urls import path

from . import views

urlpatterns = [
    path('query.html/', views.query, name='query'),
]