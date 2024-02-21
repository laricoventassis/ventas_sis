from django.conf import settings

def prefijo_url(request):
    return {'PREFIJO_URL': settings.PREFIJO_URL}



