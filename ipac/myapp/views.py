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
from email.mime.image import MIMEImage
def index(request):
    return render(request, 'myapp/index.html')
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