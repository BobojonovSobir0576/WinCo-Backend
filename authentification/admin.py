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
        (None, {"fields": ["is_varified","age","gender_id","about_me","interests","location_lat","location_lng","avatar",]}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (

        (None,{'classes': ('wide',), 'fields':('is_varified',"age","gender_id","about_me","interests","location_lat","location_lng","avatar",)}),
    )
    search_fields = ("email","username")
    ordering = ("email",)

admin.site.register(CustomUser,NewMyUser)


@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ['id','g_name']

@admin.register(CustomUserImage)
class CustomUserImageAdmin(admin.ModelAdmin):
    list_display = ['id','user_id']