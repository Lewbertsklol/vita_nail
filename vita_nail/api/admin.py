from django.contrib import admin

# Register your models here.
from api.models import Client, Window, Work


admin.site.register(Client)
admin.site.register(Window)
admin.site.register(Work)
