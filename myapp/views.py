from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.templatetags.static import static
import os
from django.utils.timezone import now
from email.mime.image import MIMEImage
from .models import ContactMessage
from django.contrib.auth import logout
import codecs
from django.db.models import Q
from itertools import groupby
from django.db.models import Count
from datetime import datetime
from django.db.models.functions import TruncDate


def index(request):
    posts = VlogPost.objects.all().order_by('-created_at')

    for post in posts:
        post.title = codecs.decode(post.title, 'unicode_escape')  # decode each title

    default_quote = Quote.objects.filter(is_default=True).first()

    return render(request, 'myapp/index.html', {
        'posts': posts,
        'default_quote': default_quote,
    })  

from django.templatetags.static import static

def seo_meta(request):
    return {
        'OG_IMAGE': request.build_absolute_uri(static('images/weblogo.jpg')),
        'SITE_TITLE': "ATTY. JAY-R IPAC",
        'SITE_DESCRIPTION': "Jayr is currently a Partner at one of the leading law firms in the Philippines. His practice areas include intellectual property, data privacy / protection, cybercrime, e-commerce law, tech contracts review, financial technology, corporate and criminal litigation, and regulatory intersections of law and technology (like blockchain and artificial intelligence).",
    }

def send_email(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')
        user_message = request.POST.get('message')

        # 🗃 Save to database
        ContactMessage.objects.create(email=user_email, message=user_message)

        # 📧 Email content
        subject = "📝 New Message from Atty. Jay-R Ipac Website"
        to_email = ['attyjayr.ipac@gmail.com']
        from_email = 'attyjayr.ipac@gmail.com'

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

        # 📤 Send email
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=to_email,
            reply_to=[user_email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

        # ✅ Feedback message
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
from django.urls import reverse
def view_article(request, post_id):
    
    post = get_object_or_404(VlogPost, id=post_id, is_article=True)

    # Absolute image URL for Open Graph
    image_url = request.build_absolute_uri(reverse('serve_post_image', args=[post.id]))

    return render(request, 'myapp/articles.html', {
        'post': post,
        'image_url': image_url  # pass to template
    })
from django.shortcuts import render
from itertools import groupby
from operator import attrgetter
from .models import VlogPost

from django.db.models import Q
from itertools import groupby
def robots_txt(request):
    content = "User-agent: *\nDisallow:\n\nSitemap: https://jayripac.com/sitemap.xml"
    return HttpResponse(content, content_type="text/plain")
# ...existing code...
def latest(request):
    query = request.GET.get('q', '')
    selected_date = request.GET.get('date', '')  # get the date filter
    posts = VlogPost.objects.all()

    # Search query filtering
    if query:
        posts = posts.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    # Date filtering using TruncDate for accurate matching
    group_by_field = 'created_at'
    if selected_date:
        try:
            date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
            posts = posts.annotate(post_date=TruncDate('created_at')).filter(post_date=date_obj)
            group_by_field = 'post_date'
        except ValueError:
            pass  # ignore invalid date format

    posts = posts.order_by('-created_at')
    posts_list = list(posts)  # Force evaluation

    # Group posts by date
    grouped_posts = []
    if group_by_field == 'post_date':
        for date, items in groupby(posts_list, key=lambda p: p.post_date):
            grouped_posts.append((date, list(items)))
    else:
        for date, items in groupby(posts_list, key=lambda p: p.created_at.date()):
            grouped_posts.append((date, list(items)))

    # Get 5 most common titles (recommended keywords)
    recommended_titles = (
        VlogPost.objects
        .values('title')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )
    recommended_keywords = [item['title'] for item in recommended_titles]

    return render(request, 'myapp/latest.html', {
        'grouped_posts': grouped_posts,
        'query': query,
        'selected_date': selected_date,
        'has_results': posts.exists(),
        'recommended_keywords': recommended_keywords,
    })



# ADMINISTRATOR

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.utils.timezone import now
from .models import VlogPost
from .models import Quote
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect

def admin_jayr(request):
    return render(request, 'myapp/administrator/index.html')

def admin_jayr(request):
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
        return redirect('manage_posts')

    return render(request, 'myapp/administrator/index.html')
def manage_posts(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            title = codecs.decode(title, 'unicode_escape')

        description = request.POST.get('description')
        url = request.POST.get('url')
        image = request.FILES.get('image')
        is_article = 'is_article' in request.POST

        VlogPost.objects.create(
            title=title,
            description=description,
            image=image,
            url=url,
            is_new=True,
            is_article=is_article
        )
        return redirect('admin_dashboard')

    posts = VlogPost.objects.all().order_by('-created_at')
    today = now().date()

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
    return redirect('manage_posts') 

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


@login_required
def manage_posts(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        title = request.POST.get('title')
        description = request.POST.get('description')
        url = request.POST.get('url')
        image = request.FILES.get('image')
        is_article = 'is_article' in request.POST

        image_data = image.read() if image else None
        image_type = image.content_type if image else ''

        if post_id:
            post = get_object_or_404(VlogPost, id=post_id)
            post.title = title
            post.description = description
            post.url = url
            post.is_article = is_article
            if image_data:
                post.image_data = image_data
                post.image_content_type = image_type
            post.save()
        else:
            VlogPost.objects.create(
                title=title,
                description=description,
                image_data=image_data,
                image_content_type=image_type,
                url=url,
                is_new=True,
                is_article=is_article
            )
        return redirect('manage_posts')

    posts = VlogPost.objects.all().order_by('-created_at')
    today = now().date()

    for post in posts:
        if post.is_new and post.created_at.date() != today:
            post.is_new = False
            post.save(update_fields=['is_new'])

    return render(request, 'myapp/administrator/posts.html', {'posts': posts})
from django.http import HttpResponse, Http404

def serve_post_image(request, post_id):
    post = get_object_or_404(VlogPost, id=post_id)

    if post.image_data:
        response = HttpResponse(post.image_data, content_type=post.image_content_type or 'image/jpeg')
        response['Content-Disposition'] = f'inline; filename="post-{post_id}.jpg"'
        return response

    raise Http404("Image not found")

@login_required
def mails(request):
    messages = ContactMessage.objects.order_by('-created_at')
    return render(request, 'myapp/administrator/mails.html', {'messages': messages})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def manage_quotes(request):
    if request.method == 'POST':
        quote_text = request.POST.get('text')
        if quote_text:
            Quote.objects.create(text=quote_text)
            return redirect('manage_quotes')

    quotes = Quote.objects.all().order_by('-created_at')
    return render(request, 'myapp/administrator/manage_quotes.html', {'quotes': quotes})


@login_required
def set_default_quote(request, quote_id):
    if request.method == 'POST':
        Quote.objects.update(is_default=False)  # Reset all
        selected = get_object_or_404(Quote, id=quote_id)
        selected.is_default = True
        selected.save()
    return redirect('manage_quotes')

def add_quote(request):
    if request.method == 'POST':
        quote_text = request.POST.get('text')
        if quote_text:
            Quote.objects.create(text=quote_text)
        return redirect('manage_quotes') 
    return render(request, 'myapp/administrator/manage_quotes.html') 
