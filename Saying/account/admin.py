from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Account


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('user_acc', 'username', 'user_status', 'user_age', 'user_gender')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("패스워드가 동일하지 않습니다.")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Account
        fields = ('user_acc', 'username', 'user_status', 'password')

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    readonly_fields = ['image_thumb']
    list_display = ('user_acc', 'username', 'user_status', 'is_active', 'is_admin', 'is_superuser')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('user_acc', 'password')}),
        ('Personal info', {'fields': ('image_thumb', 'user_profile_img', 'username', 'user_status', 'user_age', 'user_gender')}),
        ('Permissions', {'fields': ('is_admin', 'is_superuser', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_acc', 'username', 'password1', 'password2')}
        ),
    )
    search_fields = ('user_acc',)
    ordering = ('user_acc',)
    filter_horizontal = ()

admin.site.site_title = 'Saying'
admin.site.site_header = 'Saying 관리자 페이지'
admin.site.register(Account, UserAdmin)
admin.site.unregister(Group)