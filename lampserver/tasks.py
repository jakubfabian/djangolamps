from __future__ import absolute_import

from celery import shared_task,task
import time
import spidev
from lampserver.models import LEDLamp, tasktime
from itertools import cycle
from django.core.cache import cache


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
        for il, l in enumerate(lamps):
                R,G,B,_ = [ gamma_correct(i) for i in l ]
		A = l[-1]
                brightness = [ (7<<5) | int(A/255.*31) ] # first 3 ones and then 32 is full brightness dimming
		if il==131: # bad pixeln on ute's lamp
		    v+=brightness+[0,0,0]
		else:
		    v+=brightness+[B,G,R]
        #print 'brightness', brightness, '::', A

        return start+v+end


@shared_task(ignore_result=True)
def update_lamps():
    global SPI

    Nlamps = 240

    #print('Started update_lamps worker')
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


@task(ignore_result=True)
def do_cmap(fwdcolors, Nlamps, time, Ncolorsteps=8, Nmaps=22, **kwargs):
    global SPI
    revcolors = fwdcolors[::-1]

    all_colors = fwdcolors + revcolors
    all_colors *= int(Nmaps)
    all_colors = all_colors[::int(Ncolorsteps)]

    colorcycles = [ cycle( all_colors ) for i in range(Nlamps) ]

    if SPI is None:
	    SPI = spidev.SpiDev()
	    SPI.open(0,0)
	    SPI.max_speed_hz = 1250000*4

    for li,cc in enumerate(colorcycles):
        Ncycles = (li * len(all_colors)) // Nlamps  # we want to cycle the colormap forward for equidistant colors
        [ next(cc) for k in range(Ncycles) ]

    while True:
        colorlist = [ next(c) for c in colorcycles ]
        colorlist = [ [ int(c*255) for c in cl] for cl in colorlist]
        spi_send(SPI, colorlist)
        if time != tasktime.objects.order_by('id').first().time:
            # print 'Exit cmap loop bc:', time, tasktime.objects.order_by('id').first().time
            return
