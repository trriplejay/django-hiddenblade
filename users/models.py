from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
#from phonenumber_field.modelfields import PhoneNumberField
#need to import models.py from the hangouts app eventually


# Create your models here.
class MyUserManager(BaseUserManager):

    def live(self):
        return self.model.objects.filter(is_active=True)

    def create_user(
        self,
        email,
        username, 
        first_name='', 
        last_name='',
        home_address='',
        work_address='',
  #      phone_number='',
        password=None
    ):
        if not email:
            raise ValueError('You must provide an email address!')
        if not username:
            raise ValueError('You must provide a user name!')
        now = timezone.now()
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            home_address=home_address,
            work_address=work_address,
 #           phone_number=phone_number,
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
        email,
        first_name='',
        last_name='',
        home_address='',
        work_address='',
    #    phone_number='',
    ):
        user = self.create_user(
            email, 
            username=username,
            first_name=first_name,
            last_name=last_name,
            home_address=home_address,
            work_address=work_address,
   #         phone_number=phone_number,
            password=password
            
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    

class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=255, 
        verbose_name='email address',
    )
    username = models.CharField(
        max_length=255, 
        unique=True,
        verbose_name='user name',
    )

    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    home_address = models.CharField(max_length=255, blank=True)
    work_address = models.CharField(max_length=255, blank=True)
#    phone_number = PhoneNumberField(blank=True)


    date_joined = models.DateField()
#    hangouts = models.ForeignKey(Hangout)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',] 


    def get_slug_field(self):
        return self.username

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return self.first_name + ' ' +  self.last_name

    def __unicode__(self):
        return self.username


    @property
    def is_staff(self):
        return self.is_admin

    @models.permalink
    def get_absolute_url(self):
        return ("users:detail", (), { "slug": self.username})

