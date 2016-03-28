# djangolamps

A small project to control a 102c APA LED Strip.


User should have control over the lamps through a web interface.
For educational purposes we use the Django framework.

Key features are:
  - User interface is web based through Django-web framework
  - Lamp state is saved in postgresql database
  - LED's controlled through SPI on Raspberry Pi
  - asynchronous sending on SPI bus through celery, through rabbitmq.
  - Everything wrapped up in docker images
