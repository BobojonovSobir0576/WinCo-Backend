from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import *

class NewMyUser(UserAdmin):
    add_form = CreasteUser
    form = ChangeUser
    model = CustomUser
    list_display = ['username','first_name','last_name','email']
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ["is_varified"]}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (

        (None,{'classes': ('wide',), 'fields':('is_varified',)}),
    )
    search_fields = ("email","username")
    ordering = ("email",)

admin.site.register(CustomUser,NewMyUser)