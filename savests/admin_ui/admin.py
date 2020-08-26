from django.contrib import admin
from django.urls import path
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.utils.translation import ngettext

# Register your models here.
admin.site.site_header = 'SaVests Admin Dashboard'


class UserAdmin(admin.ModelAdmin):
    """Extending the Django admin dashboard page to show user metrics,
        customize action button to the users list page that enables staff
        to set a user to active or inactive with the click of a button,
        functionality  that allows staff to send an email to all existing users."""
    list_display = ('username', 'first_name', 'last_name', 'email','is_active', 'is_staff')
    list_filter = ('date_joined','last_login', 'is_active', 'is_staff')
    change_list_template = 'admin/admin_ui/admin_ui_change_list.html'
    actions = ['make_active', 'make_inactive', 'make_staff', 'remove_staff']


    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('sendmail/', self.send_mail_view)
        ]
        return my_urls + urls

    def send_mail_view(self, request):
        """View to send mail to all users"""
        users = self.model.objects.all()
        sender = request.POST['sender']
        subject = request.POST['subject']
        message = request.POST['message']
        recipient = [user.email for user in users]
        send_mail(
            subject,
            message,
            sender,
            recipient,
            fail_silently=False,
        )
        self.message_user(request, 'Mail sent successfully')
        return HttpResponseRedirect('../')
        
    
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