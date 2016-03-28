from django.shortcuts import render
from django.db import transaction
from lampserver.models import LEDLamp

from django.http import HttpResponse

# Create your views here.
def lamp_view(request, R,B,G):
    color = [R,B,G,255]
    with transaction.atomic():
        for l in LEDLamp.objects.order_by('id'):
            l.lamp_values = color
            l.save()
    html = "<html><body>It is now %s.</body></html>" % color
    return HttpResponse(html)
