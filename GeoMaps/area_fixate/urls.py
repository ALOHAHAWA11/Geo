from django.urls import path

from area_fixate.views import get_by_cadastral

urlpatterns = [
    path('cadastral/', get_by_cadastral, name='get_by_cadastral'),
]
