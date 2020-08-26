from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.contrib import messages
from django.utils.translation import ngettext

# Register your models here.
admin.site.site_header = 'SaVests Admin Dashboard'



class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email','is_active', 'is_staff')
    list_filter = ('date_joined','last_login', 'is_active', 'is_staff')
    actions = ['make_active', 'make_inactive', 'make_staff', 'remove_staff']

    def make_active(self, request, queryset):
        updated = queryset.update(is_active = True)
        self.message_user(request, ngettext(
            '%d user was successfully made active',
            '%d users were successfully made active',
            updated
        ) % updated, messages.SUCCESS)
    
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active = False)
        self.message_user(request, ngettext(
            '%d user was successfully made inactive',
            '%d users were successfully made inactive',
            updated
        ) % updated, messages.SUCCESS)
    
    def make_staff(self, request, queryset):
        updated = queryset.update(is_staff = True)
        self.message_user(request, ngettext(
            '%d user was successfully made a staff',
            '%d users were successfully made staffs',
            updated
        ) % updated, messages.SUCCESS)
    
    def remove_staff(self, request, queryset):
        updated = queryset.update(is_staff = False)
        self.message_user(request, ngettext(
            '%d user is no longer a staff',
            '%d users are no longer staffs',
            updated
        ) % updated, messages.SUCCESS)
    
    make_active.short_description = "Make selected users active"
    make_inactive.short_description = "Make selected users inactive"
    make_staff.short_description = "Make selected users a staff"
    remove_staff.short_description = "Remove staff status from selected users"
    
    


admin.site.unregister(User)
admin.site.register(User, UserAdmin)