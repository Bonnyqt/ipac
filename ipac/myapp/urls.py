# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('send-email/', views.send_email, name='send_email'),
    path('lawyer', views.lawyer, name='lawyer'),
    path('law_academe', views.law_academe, name='law_academe'),
]
