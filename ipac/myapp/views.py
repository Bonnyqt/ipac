from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.html import strip_tags
from django.templatetags.static import static
import os
from django.utils.timezone import now
from email.mime.image import MIMEImage
def index(request):
    posts = VlogPost.objects.all().order_by('-created_at')
    return render(request, 'myapp/index.html', {'posts': posts})
def about(request):
    return render(request, 'myapp/about.html')


def send_email(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')
        user_message = request.POST.get('message')

        subject = "📝 New Message from Atty. Jay-R Ipac Website"
        to_email = ['marquezjonbon@gmail.com']
        from_email = 'rafolslenelyn10@gmail.com'
     
        html_content = f"""
<div style="font-family: Arial, sans-serif; color: #333;">

  <p><strong>You received a new message from:</strong> <a href="mailto:{user_email}">{user_email}</a></p>
  <hr style="border: none; border-top: 1px solid #ccc;" />
  <div style="margin-top: 15px;">
    <p style="white-space: pre-line;">{user_message}</p>
  </div>
  <hr style="border: none; border-top: 1px dashed #bbb; margin-top: 30px;" />
  <p style="font-size: 12px; color: #999;">This message was submitted via the website contact form.</p>
</div>
"""

        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=to_email,
            reply_to=[user_email],
        )
        email.attach_alternative(html_content, "text/html")


        email.send()
        messages.success(request, "Your message has been sent successfully!")
        return redirect(request.META.get('HTTP_REFERER', '/'))

def lawyer(request):
    return render(request, 'myapp/lawyer.html')
def law_academe(request):
    return render(request, 'myapp/law_academe.html')
def author(request):
    return render(request, 'myapp/author.html')
def rotarian(request):
    return render(request, 'myapp/rotarian.html')
def beyond_the_bar(request):
    return render(request, 'myapp/beyond.html')
def chevening_alumnus(request):
    return render(request, 'myapp/chevening.html')
def eco_waste_advocate(request):
    return render(request, 'myapp/ecowaste.html')
def admin(request):
    return render(request, 'myapp/administrator/index.html')


# ADMINISTRATOR

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.utils.timezone import now
from .models import VlogPost
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect

def admin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'myapp/administrator/index.html', {
                'error': 'No user found with that email.'
            })


        user = authenticate(request, username=user.username, password=password)

        if user is None:
            return render(request, 'myapp/administrator/index.html', {
                'error': 'Incorrect password.'
            })

        if not user.is_superuser:
            return render(request, 'myapp/administrator/index.html', {
                'error': 'You are not authorized to access this page.'
            })

        # All good
        login(request, user)
        return redirect('admin_dashboard')

    return render(request, 'myapp/administrator/index.html')
def manage_posts(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        url = request.POST.get('url')
        image = request.FILES.get('image')

        # Always mark new posts as "new" on creation
        VlogPost.objects.create(
            title=title,
            description=description,
            image=image,
            url=url,
            is_new=True
        )
        return redirect('admin_dashboard')

    posts = VlogPost.objects.all().order_by('-created_at')
    today = now().date()

    # Update any posts that are no longer new
    for post in posts:
        if post.is_new and post.created_at.date() != today:
            post.is_new = False
            post.save(update_fields=['is_new'])

    return render(request, 'myapp/administrator/posts.html', {'posts': posts})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_post(request, post_id):
    post = get_object_or_404(VlogPost, id=post_id)
    if request.method == 'POST':
        post.delete()
    return redirect('admin_dashboard')  # or wherever you want to go back

def superuser_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("You are not authorized to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@superuser_required
def admin_dashboard(request):
    posts = VlogPost.objects.all().order_by('-created_at')
    return render(request, 'myapp/administrator/dashboard.html', {'posts': posts})
