from locale import normalize
from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError('email must be set')
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if (extra_fields.get('is_staff') is not True):
            raise ValueError('super user must have is_staff=true')

        if (extra_fields.get('is_superuser') is not True):
            raise ValueError('super user must have is_superuser=true')

        return self.create_user(email, password, **extra_fields)

    def get_full_name(self):

        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()


ROLECHOICE = [('student', 'student'), ('faculty', 'faculty')]


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = None

    email = models.EmailField(unique=True, max_length=200)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    role = models.CharField(choices=ROLECHOICE, max_length=10)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        return True

    @property
    def is_admin(self):
        return self.admin

    def __str__(self):
        return self.email


STUDYMODECHOICE = [('online', 'online'), ('on-campus', 'on-campus')]
STATUSCHOICE = [('none', 'none'), ('accepted', 'accepted'),
                ('rejected', 'rejected')]


class ApplicationModel(models.Model):
    app_id = models.AutoField(primary_key=True, auto_created=True)
    uni_name = models.CharField(max_length=200)
    program_name = models.CharField(max_length=200)
    study_mode = models.CharField(choices=STUDYMODECHOICE, max_length=20)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUSCHOICE,
                              max_length=20, default='none')
    description = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.customer.first_name
