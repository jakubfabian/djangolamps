from django.shortcuts import render
from django.db import transaction
from lampserver.models import LEDLamp

from django.http import HttpResponse
from .tasks import update_lamps

# Create your views here.
def lamp_view(request, **kwargs):
    print kwargs
    color = LEDLamp.objects.order_by('id')[0].lamp_values

    if 'R' in kwargs:
        color[0] = kwargs['R']
    if 'G' in kwargs:
        color[1] = kwargs['G']
    if 'B' in kwargs:
        color[2] = kwargs['B']
    if 'A' in kwargs:
        color[3] = kwargs['A']

    with transaction.atomic():
        for l in LEDLamp.objects.order_by('id'):
            l.lamp_values = color
            l.save()
    print 'Current color to be set:', LEDLamp.objects.order_by('id')[0].lamp_values
    update_lamps()
    context = {'color':color,}

    if request.is_ajax():
        html = "Ajax updated colors to ... {}".format(color)
        return HttpResponse(html)
        
    return render(request, 'lampserver/lamp_view.html', context)
