from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
#need to import models.py from the hangouts app eventually


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        username, 
        first_name='', 
        last_name='',
        password=None
    ):
        if not email:
            raise ValueError('You must provide an email address!')
        if not username:
            raise ValueError('You must provide an email address!')
        now = timezone.now()
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            last_login=now,
            is_active=True,
            date_joined=now,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        username, 
        password,
    ):
        email = 'test@example.com'
        user = self.create_user(email, username=username, password=password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    home_address = models.CharField(max_length=255, blank=True)
    work_address = models.CharField(max_length=255, blank=True)
#    last_login = models.DateField()
    date_joined = models.DateField(auto_now_add=True)
#    hangouts = models.ForeignKey(Hangout)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'username'

    def get_short_name(self):
        return self.first_name

    def get_long_name(self):
        return self.first_name + ' ' +  self.last_name

    def __unicode__(self):
        return self.username


    @property
    def is_staff(self):
        return self.is_admin
