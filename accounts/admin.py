from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

# Register your models here.
class AccountAdmin(UserAdmin):
  list_display = ('email', 'first_name', 'last_name', 'last_login', 'date_joined', 'is_active')
  ordering = ('-date_joined',)

  list_filter = ()
  filter_horizontal = ()
  fieldsets = ()

admin.site.register(Account, AccountAdmin)