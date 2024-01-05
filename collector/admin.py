from django.contrib import admin
from .models import SystemInformation, SoftwareInformation, HardwareInformation

admin.site.register(SystemInformation)
admin.site.register(SoftwareInformation)
admin.site.register(HardwareInformation)

