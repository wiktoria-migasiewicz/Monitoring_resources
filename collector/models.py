from django.db import models


class SystemInformation(models.Model):

    objects = None
    USER = models.CharField(max_length=200)
    SYSTEM = models.CharField(max_length=200)
    VERSION = models.CharField(max_length=200)
    MACHINE = models.CharField(max_length=200)
    ARCHITECTURE = models.CharField(max_length=200)
    ENVIRONMENT = models.CharField(max_length=200)
    HOSTNAME = models.CharField(max_length=200)
    PROCESSOR = models.CharField(max_length=200)


class SoftwareInformation(models.Model):
    objects = None
    USER = models.CharField(max_length=200)
    INFO1 = models.CharField(max_length=200)
    INFO2 = models.CharField(max_length=200)
    INFO3 = models.CharField(max_length=200)


class HardwareInformation(models.Model):
    objects = None
    USER = models.CharField(max_length=200)
    CPU_USAGE = models.CharField(max_length=200)
    CPU_FREQUENCY = models.CharField(max_length=200)
    RAM = models.CharField(max_length=200)
    HDD_TOTAL = models.CharField(max_length=200)
