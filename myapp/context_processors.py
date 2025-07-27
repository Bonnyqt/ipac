from django.templatetags.static import static

def global_meta(request):
    return {
        'SITE_TITLE': 'JAY-R IPAC',
        'SITE_DESCRIPTION': 'Jayr is currently a Partner at one of the leading law firms in the Philippines. His practice areas include intellectual property, data privacy / protection, cybercrime, e-commerce law, tech contracts review, financial technology, corporate and criminal litigation, and regulatory intersections of law and technology (like blockchain and artificial intelligence).',
        'OG_IMAGE': request.build_absolute_uri(static('images/weblogo.png')),
    }