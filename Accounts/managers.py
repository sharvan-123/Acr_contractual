from django.contrib.auth.base_user import BaseUserManager
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _
# from .models import CustomUser

class CustomUserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, empCode, password, **extra_fields):
        if not empCode:
            raise ValueError(_('The Employee Code must be set'))
        empCode = self.normalize_email(empCode)
        user = self.model(empCode=empCode, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, empCode, password, **extra_fields):
        if not empCode:
            raise ValueError(_('The Employee Code must be set'))
        empCode = self.normalize_email(empCode)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('empId', 1)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(empCode, password, **extra_fields)


    # create_superuser(empCode='123456', email='admin@example.com', mobile='1234567890', password='password@123')
