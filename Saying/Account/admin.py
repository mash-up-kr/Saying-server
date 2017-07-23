from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import UserCredential, UserProfile, Users


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserCredential
        fields = ('user_acc',)

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
        model = UserCredential
        fields = ('user_acc', 'password')

    def clean_password(self):
        return self.initial["password"]


class UsersInline(admin.StackedInline):
    model = Users
    can_delete = False
    verbose_name = 'hello'


class ProfileInline(admin.StackedInline):
    readonly_fields = ['profile_preview']
    fieldsets = (
        (None, {'fields': ('profile_preview', 'nickname', 'age', 'gender')}),
    )

    model = UserProfile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (UsersInline, ProfileInline,)
    form = UserChangeForm
    add_form = UserCreationForm

    list_select_related = ('userprofile', )
    list_display = ('user_acc', 'get_nickname', 'is_active', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('user_acc', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_superuser', 'is_active')}),
    )
    ordering = ('user_acc',)
    filter_horizontal = ()

    def get_nickname(self, instance):
        return instance.userprofile.nickname

    get_nickname.short_description = '닉네임'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)


admin.site.site_title = 'Saying'
admin.site.site_header = 'Saying 관리자 페이지'
admin.site.register(UserCredential, UserAdmin)
admin.site.unregister(Group)
