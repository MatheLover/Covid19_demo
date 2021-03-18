from django.urls import path

from . import views

urlpatterns = [
    path('query.html/', views.query, name='query'),
    path('about.html/', views.about, name='about'),
    path('covid19_map.html', views.covid19_map, name='covid19_map'),
    path('covid19_public_health_authority_response.html', views.covid19_public_health_authority_response,
         name='public_health_authority_response'),
    path('covid19_public_health_facility.html', views.covid19_public_health_facility,
         name='covid19_public_health_facility'),
    path('covid19_public_health_statistics.html', views.covid19_public_health_statistics,
         name='covid19_public_health_statistics'),
    path('covid19_socioeconomic_factor.html', views.covid19_socioeconomic_factor,
         name='covid19_socioeconomic_factor')
]
