# djangolamps

A small project to control a 102c APA LED Strip.
Lamps are controlled from a Raspberry Pi through the SPI-bus.
User should have control over the lamps through a web interface.
For educational purposes we use the Django framework.

Lamp state is saved in postgresql database and lamp values are update asynchronously by celery task over SPI.
