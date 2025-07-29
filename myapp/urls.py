# myapp/urls.py

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings
from django.urls import re_path
from django.contrib.sitemaps.views import sitemap
from .sitemaps import PostSitemap
from django.views.generic import TemplateView
sitemaps = {
    'posts': PostSitemap,
}


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
    
    path('post/image/<int:post_id>/', views.serve_post_image, name='serve_post_image'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path("googleb80ef680ea35a164.html", TemplateView.as_view(template_name="googleb80ef680ea35a164.html",content_type="text/html")),
    path("robots.txt", views.robots_txt),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Serve media files in production (not for large scale, just for quick test)
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
