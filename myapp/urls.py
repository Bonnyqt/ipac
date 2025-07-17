# myapp/urls.py

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

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
    path('admin_jayr', views.admin_jayr, name='admin_jayr'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-posts/', views.manage_posts, name='manage_posts'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),
     path('article/<int:post_id>/', views.view_article, name='view_article'),
     path('latest', views.latest, name='latest'),
    path('manage_posts/', views.manage_posts, name='manage_posts'),
     path('mails', views.mails, name='mails'),
     path('logout/', views.logout_view, name='logout'),
      path('manage_quotes', views.manage_quotes, name='manage_quotes'),
      path('add-quote/', views.add_quote, name='add_quote'),
          path('set-default-quote/<int:quote_id>/', views.set_default_quote, name='set_default_quote'),
]