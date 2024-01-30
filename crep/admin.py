from django.contrib import admin
from .models import Province, Municipality, Ward, Councilor, Services, Rating
# Register your models here.

admin.site.register(Province)
admin.site.register(Municipality)
admin.site.register(Ward)
admin.site.register(Councilor)
admin.site.register(Services)
admin.site.register(Rating)

