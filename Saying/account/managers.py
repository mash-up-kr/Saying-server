from django.contrib.auth.models import BaseUserManager


class AccountManager(BaseUserManager):
    def create_user(self, user_acc, username, password=None):
        user = self.model(
            user_acc=self.normalize_email(user_acc),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_acc, username, password=None):
        user = self.create_user(
            user_acc=user_acc,
            username=username,
            password=password,
        )
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user