from django.contrib import admin
from .models import Councilor, Services, Rating
# Register your models here.

admin.site.register(Councilor)
admin.site.register(Services)
admin.site.register(Rating)
