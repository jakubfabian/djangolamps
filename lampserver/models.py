from __future__ import unicode_literals

from django.db import models

# Create your models here.

import dbarray

class LEDLamp(models.Model):
    lamp_values = dbarray.IntegerArrayField(null=True)
