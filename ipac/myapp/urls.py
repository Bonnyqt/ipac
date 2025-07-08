# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('send-email/', views.send_email, name='send_email'),
    path('lawyer', views.lawyer, name='lawyer'),
    path('law_academe', views.law_academe, name='law_academe'),
    path('author', views.author, name='author'),
    path('rotarian', views.rotarian, name='rotarian'),
    path('beyond_the_bar', views.beyond_the_bar, name='beyond_the_bar'),
    path('chevening_alumnus', views.chevening_alumnus, name='chevening_alumnus'),
    path('eco_waste_advocate', views.eco_waste_advocate, name='eco_waste_advocate'),
    path('admin', views.admin, name='admin'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-posts/', views.manage_posts, name='manage_posts'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),
     path('article/<int:post_id>/', views.view_article, name='view_article'),
     path('latest', views.latest, name='latest'),
]
