from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django.contrib.auth import get_user_model

UserModel = get_user_model()

class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users, Includes all the required fields, plus a repeated password
    """
    pasaword1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    pasaword2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = ('user_login', 'email')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ('user_login', 'email', 'user_pass', 'is_active', 'is_admin')


class UserAdmin(admin.ModelAdmin):
    form = UserChangeForm
    # add_form = UserCreationForm

    # The fields to be usesd in displaying the User model
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User
    list_display = ('user_login', 'email', 'is_admin')
    list_filter = ('is_admin', )
    fieldsets = (
        (None, {'fields': ('user_login', 'user_pass', 'email')}),
        ('Personal info', {'fields': ('user_nicename', 'user_status')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')})
    )
    readonly_fields = ('user_pass',)

    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields' : ('user_login', 'email', 'password1', 'password2')
    #     })
    # )

    search_fields = ('email', 'user_login')
    ordering = ('user_login', 'email')
    filter_horizental = ()

admin.site.register(UserModel, UserAdmin)
admin.site.unregister(Group)