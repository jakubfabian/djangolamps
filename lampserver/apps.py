from __future__ import unicode_literals

from django.apps import AppConfig

def start_lamp_updater():
    """
    Run celery update lamps thread
    """
    import lampserver.tasks as L
    L.update_lamps.delay()

class LampserverConfig(AppConfig):
    name = 'lampserver'
    RUN_LAMP_UPDATER = True
    def ready(self):
        pass # startup code here
	if self.RUN_LAMP_UPDATER:
	    start_lamp_updater()
            self.RUN_LAMP_UPDATER = False
