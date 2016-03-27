from __future__ import absolute_import

from celery import shared_task
import time


@shared_task
def update_lamps(N):

    for i in range(N):
	    time.sleep(5)
	    print('Updating lamps...',i,'//',N)
    return N
