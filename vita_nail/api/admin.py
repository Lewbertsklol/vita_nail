from django.contrib import admin

# Register your models here.
from api.models import Client, Window, Procedure


admin.site.register(Client)
admin.site.register(Window)
admin.site.register(Procedure)
