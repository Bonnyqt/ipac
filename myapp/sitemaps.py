from django.contrib.sitemaps import Sitemap
from .models import VlogPost  # or your model

class PostSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return VlogPost.objects.all()

    def lastmod(self, obj):
        return obj.updated_at  # use your timestamp field
