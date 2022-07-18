from django.urls import path
from . import views





urlpatterns = [
	path('', views.home, name='firstapp-home'),
	path('about/', views.about, name='firstapp-about'),
]