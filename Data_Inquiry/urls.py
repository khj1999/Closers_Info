from django.urls import path
from . import views

urlpatterns = [
    path('character_search/', views.character_search, name='character_search'),
    path('search/ajax/', views.character_search_ajax, name='character_search_ajax'),
]