from django.db import models


class VlogPost(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='vlog_images/')
    url = models.URLField(max_length=500, blank=True)
    is_new = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_article = models.BooleanField(default=False)
    def __str__(self):
        return self.title

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
    