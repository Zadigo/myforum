from accounts import forms
from accounts.models import MyUser, PermanentBan, TemporaryBan, UserProfile
from django.contrib import admin
from django.contrib.auth.forms import AdminPasswordChangeForm


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    form = forms.CustomUserChangeForm
    add_form = forms.CustomUserCreationForm
    # change_password_form = AdminPasswordChangeForm
    add_form_template = 'admin/auth/user/add_form.html'
    list_display = ['username', 'email', 'get_full_name', 'is_active']
    search_fields = ['email', 'first_name', 'last_name']
    list_filter = ['is_active', 'is_staff', 'is_moderator']
    date_hierarchy = 'date_joined'
    filter_horizontal = ['user_permissions']

    def get_form(self, request, obj=None, **kwargs):
        """Use special form for user creation"""
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_premium']
    date_hierarchy = 'created_on'


@admin.register(TemporaryBan)
class TemporarilyBannedUserAdmin(admin.ModelAdmin):
    list_display = ['number_of_days', 'start_date',
                    'end_date', 'reason', 'appealed']


@admin.register(PermanentBan)
class PermanentlyBannedUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'reason', 'appealed']
