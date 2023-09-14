from django.conf import settings
from django.contrib.sites.models import Site
from django.utils import timezone


def main_context(request):
    if not request.session.exists(request.session.session_key):
        request.session.create()

    domain = request.META.get("HTTP_HOST", "")
    site_name = "aahaglobal"
    logo_url = "/static/main/images/logo.png"
    favicon_url = "/static/main/images/logo_mini.svg"

    if not Site.objects.filter(pk=settings.SITE_ID).exists():
        new_site = Site(pk=settings.SITE_ID, domain=domain, name=site_name)
        new_site.save()

    if request.user.is_authenticated:
        if request.user.is_superuser:
            usertype = "Administator"
        else:
            usertype = "Textiles"
    else:
        usertype = "Guest"
    return {
        "domain": domain,
        "site_name": site_name,
        "logo_url": logo_url,
        "favicon_url": favicon_url,
        "usertype": usertype,
        "domain": "http://aahaaglobal.com",
    }
