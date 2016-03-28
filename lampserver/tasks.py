from __future__ import absolute_import

from celery import shared_task
import time
import spidev

def spi_send(spi, lamps):
    v = lamp_values(lamps)
    return spi.xfer(v)

def gamma_correct(inp):
    gamma = 2.8
    return int( (inp/255.)**gamma * 255 + .5)

def lamp_values(lamps):
        start = [0]*4
        end = [255]*(4*(len(lamps)//64+1)) # 4 byte end for each 64 lamps
        v = []
        for l in lamps:
                R,G,B,A = [ gamma_correct(i) for i in l ]
                #brightness = [ (7<<5)| int(A/255.*7) ] # first 4 ones and then 63 is full brightness dimming
                brightness = [ (7<<5)| 63 ] # first 4 ones and then 63 is full brightness dimming
                brightness = [ (7<<5)| 1 ] # first 4 ones and then 63 is full brightness dimming
                v+=brightness+[B,G,R]

        return start+v+end

@shared_task
def update_lamps():
    print('Started update_lamps worker')
    time.sleep(1) # wait till everything is up and running
    from lampserver.models import LEDLamp
    lamps = LEDLamp.objects.all()

    Nlamps = 300

    if len(lamps)!=Nlamps:
        [ l.delete() for l in lamps ]
        [ LEDLamp(id=i, lamp_values=[255,255,255,255]).save() for i in range(300) ]

    spi = spidev.SpiDev()

    spi.open(0,0)
    spi.max_speed_hz = 1250000*4
    
    while True:
        lamp_vals = [ l.lamp_values for l in LEDLamp.objects.order_by('id') ]
	spi_send(spi, lamp_vals)
	time.sleep(1e-2)
        
    return
