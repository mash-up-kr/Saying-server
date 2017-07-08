import uuid
from django.db import models
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import AbstractBaseUser
from django.core.urlresolvers import reverse_lazy
from .managers import AccountManager

status_types = (
    (1, '정상'),
    (2, '임시'),
    (3, '휴면'),
    (4, '탈퇴'),
)

age_types = (
    (1, '10대'),
    (2, '20대'),
    (3, '30대'),
    (4, '40대이상'),
)

gender_types = (
    (1, '남'),
    (2, '여'),
)


class TimeStampedModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Account(AbstractBaseUser, TimeStampedModel):
    id = models.UUIDField(
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
    username = models.CharField(
        "닉네임",
        max_length=20,
        default=""
    )
    user_profile_img = models.ImageField(
        "프로필 사진",
        upload_to='profile',
        default="profile/default.png"
    )
    user_status = models.SmallIntegerField(
        "계정상태",
        choices=status_types,
        default=2
    )
    user_age = models.SmallIntegerField(
        "나이",
        choices=age_types,
        default=2
    )
    user_gender = models.SmallIntegerField(
        "성별",
        choices=gender_types,
        default=2
    )

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'user_acc'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return "username: " + self.username

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
        return self.username

    def get_absolute_url(self):
        url = reverse_lazy('detail', kwargs={'pk': self.pk})
        print(url)
        return url

    def image_thumb(self):
        return '<img src="%s" width="100" height="100" />' % self.user_profile_img.url

    image_thumb.short_description = 'Preview'
    image_thumb.allow_tags = True
