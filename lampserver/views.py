from django.shortcuts import render
from django.db import transaction
from lampserver.models import LEDLamp

from django.http import HttpResponse

# Create your views here.
def lamp_view(request, R,B,G):
    color = [ int(x) for x in [R,B,G,255]]
    with transaction.atomic():
        for l in LEDLamp.objects.order_by('id'):
            l.lamp_values = color
            l.save()
    context = {'color':color,}
    return render(request, 'lampserver/lamp_view.html', context)
