from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from accounts.models import Profile
from .models import User


class AddUserForm(forms.ModelForm):
    """
    New User Form. Requires password confirmation.
    """
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UpdateUserForm(forms.ModelForm):
    """
    Update User Form. Doesn't allow changing password in the Admin.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'email', 'username', 'password', 'first_name', 'last_name', 'is_active',
            'is_staff'
        )

    def clean_password(self):
        # Password can't be changed in the admin
        return self.initial["password"]


class UsersProfileAdmin(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class UserAdmin(BaseUserAdmin):

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

    inlines = (UsersProfileAdmin,)
    form = UpdateUserForm
    add_form = AddUserForm
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'get_profession')
    list_select_related = ('profile',)
    list_filter = ('is_staff',)
    search_fields = ('email', 'username', 'first_name')
    ordering = ('email', 'first_name', 'username')
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email', 'username', 'first_name', 'last_name', 'password1',
                    'password2'
                )
            }
        ),
    )

    def get_profession(self, instance):
        return '{}'.format(instance.profile.profession).title()

    get_profession.short_description = 'profession'
    list_display_links = ('email', 'username',)


admin.site.register(User, UserAdmin)
