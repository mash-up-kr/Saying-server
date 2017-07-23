from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, user_acc, password=None):

        user = self.model(
            user_acc=self.normalize_email(user_acc),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_acc, password=None):
        user = self.create_user(
            user_acc=user_acc,
            password=password,
        )
        user.is_superuser = True
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user
