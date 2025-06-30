# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('send-email/', views.send_email, name='send_email'),
    path('lawyer', views.lawyer, name='lawyer'),
    path('law_academe', views.law_academe, name='law_academe'),
    path('author', views.author, name='author'),
    path('rotarian', views.rotarian, name='rotarian'),
    path('beyond_the_bar', views.beyond_the_bar, name='beyond_the_bar'),
    path('chevening_alumnus', views.chevening_alumnus, name='chevening_alumnus'),
    path('eco_waste_advocate', views.eco_waste_advocate, name='eco_waste_advocate'),
]
