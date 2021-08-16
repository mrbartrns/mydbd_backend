from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import *

# Register your models here.
admin.site.register(Killer)
admin.site.register(Survivor)
admin.site.register(Owner)
