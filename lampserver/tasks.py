from __future__ import absolute_import

from celery import shared_task
import time


@shared_task
def update_lamps():
    print('Started update_lamps worker')
    time.sleep(5) # wait till everything is up and running
    from lampserver.models import LEDLamp
    lamps = LEDLamp.objects.all()
    for i,l in enumerate(lamps):
	    time.sleep(1)
	    print('Updating lamps...',i,'//',len(lamps),l,'::',l.lamp_values)
    return
