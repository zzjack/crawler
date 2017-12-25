from django.contrib import admin
from .models import Hd_EMD008, Hd_EMR002

# Register your models here.
class HdEMD008(admin.ModelAdmin):
    list_display = ("name","idcard")

admin.site.register(Hd_EMD008)
admin.site.register(Hd_EMR002)
