import uuid
from django.db import models
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.urlresolvers import reverse_lazy
from django.dispatch import receiver
from django.db.models.signals import post_save

from .managers import UserManager
from .choice_type import status_types, age_types, gender_types


class UserCredential(AbstractBaseUser, PermissionsMixin):
    userid = models.CharField(
        max_length=36,
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user_acc = models.EmailField(
        "계정명(이메일 형태)",
        max_length=255,
        default="",
        unique=True,
    )
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'user_acc'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.userid

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def has_module_perms(self, app_label):
        """
        Returns True if the user has any permissions in the given app label.
        Uses pretty much the same logic as has_perm, above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True
        return auth_models._user_has_module_perms(self, app_label)

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True
        return auth_models._user_has_perm(self, perm, obj)

    def get_short_name(self):
        return self.user_acc

    def get_full_name(self):
        return self.userid


class UserProfile(models.Model):
    userid = models.OneToOneField(
        UserCredential,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    nickname = models.CharField(
        "닉네임",
        max_length=20,
        default=""
    )
    user_profile_img = models.ImageField(
        "프로필 사진",
        upload_to='profile',
        default="profile/default.png"
    )
    age = models.SmallIntegerField(
        "나이",
        choices=age_types,
        default=2
    )
    gender = models.SmallIntegerField(
        "성별",
        choices=gender_types,
        default=2
    )
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.userid.user_acc

    def get_absolute_url(self):
        url = reverse_lazy('detail', kwargs={'pk': self.pk})
        print(url)
        return url

    def profile_preview(self):
        return '<img src="%s" width="100" height="100" />' % self.user_profile_img.url

    profile_preview.short_description = 'Preview'
    profile_preview.allow_tags = True


class Users(models.Model):
    userid = models.OneToOneField(
        UserCredential,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    user_status = models.SmallIntegerField(
        "계정상태",
        choices=status_types,
        default=2
    )
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.userid.user_acc


@receiver(post_save, sender=UserCredential)
def create_or_update_user(sender, instance, created, **kwargs):
    if created:
        Users.objects.create(userid=instance)
        UserProfile.objects.create(userid=instance)
    instance.userprofile.save()
    instance.users.save()
