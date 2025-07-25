from django.db import models

from django.urls import reverse

class VlogPost(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image_data = models.BinaryField(blank=True, null=True)
    image_content_type = models.CharField(max_length=100, blank=True)
    url = models.URLField(max_length=500, blank=True)
    is_new = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_article = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('view_article', kwargs={'post_id': self.pk})
class ContactMessage(models.Model):
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.email}"

class Quote(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.text[:50]
    