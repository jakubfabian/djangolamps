from __future__ import absolute_import

from celery import shared_task
import time
import spidev
from lampserver.models import LEDLamp


SPI=None


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
                brightness = [ (15<<5)| 63 ] # first 4 ones and then 63 is full brightness dimming
                brightness = [ (15<<5)| 1 ] # first 4 ones and then 63 is full brightness dimming
                brightness = [ (15<<5)| int(A/255.*15+.5) ] # first 4 ones and then 63 is full brightness dimming
                v+=brightness+[B,G,R]
        print 'brightness', brightness

        return start+v+end


@shared_task(ignore_result=True)
def update_lamps():
    global SPI

    Nlamps = 300

    print('Started update_lamps worker')
    lamps = LEDLamp.objects.all()

    if len(lamps)!=Nlamps:
        [ l.delete() for l in lamps ]
        [ LEDLamp(id=i, lamp_values=[255,255,255,255]).save() for i in range(Nlamps) ]

    if SPI is None:
	    SPI = spidev.SpiDev()
	    SPI.open(0,0)
	    SPI.max_speed_hz = 1250000*4
    
    #while True:
    lamp_vals = [ l.lamp_values for l in LEDLamp.objects.order_by('id') ]
    spi_send(SPI, lamp_vals)
    #time.sleep(1e-2)
        
    return
