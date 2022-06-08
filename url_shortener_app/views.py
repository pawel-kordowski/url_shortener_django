from django.http import Http404
from django.shortcuts import redirect
from django.views.decorators.http import require_GET

from url_shortener_app.models import Url


@require_GET
def get_redirect(request, short: str):
    try:
        url = Url.objects.get(short=short)
    except Url.DoesNotExist:
        raise Http404()
    return redirect(url.url)
