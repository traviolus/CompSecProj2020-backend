from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _

class CustomUserManager(BaseUserManager) :
    def create_user(self, user_name, password, user_email, **kwargs) :
        if not user_name :
            raise ValueError(_('The Username must be set.'))
        user = self.model(user_name=user_name, **kwargs)
        user.user_email = user_email
        user.user_status = 2
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, user_name, password, user_email, **kwargs) :
        user = self.create_user(user_name, password, user_email, **kwargs)
        user.user_status = 1
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
