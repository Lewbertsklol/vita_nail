from django.contrib import admin

# Register your models here.
from api.models import User, Window, Work


admin.site.register(User)
admin.site.register(Window)
admin.site.register(Work)
