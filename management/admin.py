from django.contrib import admin
from .models import MyUser, Organization
# Register your models here.


class MyUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'email_domain','organization']

admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Organization)