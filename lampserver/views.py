from django.shortcuts import render
from django.db import transaction
from lampserver.models import LEDLamp, tasktime

from django.http import HttpResponse
from .tasks import update_lamps, do_cmap
import time


def update_commando_time():
    timestamp = int(time.time())
    t = tasktime.objects.first()
    t.time = timestamp
    t.save()
    return timestamp



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

    update_commando_time()
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


def cmap(request, **kwargs):
    from matplotlib.pyplot import get_cmap
    from matplotlib import pyplot as plt

    maps = sorted(m for m in plt.cm.datad if not m.endswith("_r"))

    cmap_name   = kwargs['cmname']      if 'cmname'      in kwargs else 'jet'
    alpha       = kwargs['alpha']       if 'alpha'       in kwargs else 127
    Ncolorsteps = kwargs['Ncolorsteps'] if 'Ncolorsteps' in kwargs else 1
    Nmaps       = kwargs['Nmaps']       if 'Nmaps'       in kwargs else 22

    cmap = get_cmap(cmap_name)
    colors = [ cmap(i) for i in range(cmap.N) ]
    for i,c in enumerate(colors):
        colors[i] = c[:3] + (c[3]*int(alpha)/255.,)

    do_cmap.delay(colors, 300, update_commando_time(), Ncolorsteps, Nmaps)

    context = {'cmap_name':cmap_name,
               'alpha':alpha,
               'Ncolorsteps':Ncolorsteps,
               'Nmaps':Nmaps,
               'cmaplist':maps,
              }
    return render(request, 'lampserver/cmap_view.html', context)
    return HttpResponse("you called me ... {}".format(kwargs))




