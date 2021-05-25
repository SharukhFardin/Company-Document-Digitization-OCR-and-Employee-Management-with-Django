from django.contrib import admin

from .models import Plan_User, User_Role, User_Group
# Register your models here.

admin.site.register(Plan_User)
admin.site.register(User_Role)
admin.site.register(User_Group)
