from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get-report', views.get_report, name='get_report'),

    
]
