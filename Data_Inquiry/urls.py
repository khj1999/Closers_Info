from django.urls import path
from . import views

urlpatterns = [
    path('character_search/', views.character_search, name='character_search'),
    path('search/ajax/', views.character_search_ajax, name='character_search_ajax'),
    
    path('ranking_list/', views.ranking_list, name='ranking_list'),
    path('ranking/ajax/', views.ranking_list_ajax, name='ranking_list_ajax'),
]