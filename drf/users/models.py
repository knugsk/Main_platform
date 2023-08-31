from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, stu_id, first_name, last_name, password=None):
        if not stu_id or not first_name or not last_name:
            raise ValueError('stu_id, first_name, and last_name must be set')
        user = self.model(stu_id=stu_id, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, stu_id, first_name, last_name, password=None):
        user = self.create_user(stu_id, first_name, last_name, password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    stu_id = models.CharField(max_length=10, unique=True, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'stu_id'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.stu_id

    def get_full_name(self):
        return f"{self.last_name} {self.first_name}"

    def get_short_name(self):
        return self.first_name
