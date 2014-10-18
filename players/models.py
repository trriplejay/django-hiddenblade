from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
#need to import models.py from the hangouts app eventually



# Create your models here.
class PlayerManager(BaseUserManager):

    def live(self):
        return self.model.objects.filter(is_active=True)

    def create_player(
        self,
        email,
        username,
        first_name='',
        last_name='',
        home_address='',
        home_zip='',
        work_address='',
        work_zip='',
        phone_number='',
        password=None
    ):
        if not email:
            raise ValueError('You must provide an email address!')
        if not username:
            raise ValueError('You must provide a user name!')
        now = timezone.now()
        player = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            home_address=home_address,
            home_zip=home_zip,
            work_address=work_address,
            work_zip=work_zip,
            phone_number=phone_number,
            last_login=now,
            is_active=True,
        )

        player.set_password(password)
        player.save(using=self._db)
        return player

    def create_superuser(
        self,
        username,
        password,
        email,
        first_name='',
        last_name='',
        home_address='',
        home_zip='',
        work_address='',
        work_zip='',
        phone_number='',
    ):
        user = self.create_player(
            email,
            username,
            first_name=first_name,
            last_name=last_name,
            home_address=home_address,
            home_zip=home_zip,
            work_address=work_address,
            work_zip=work_zip,
            phone_number=phone_number,
            password=password

        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Player(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=255,
        verbose_name='email address',
    )
    username = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='user name',
    )
    zip_regex = RegexValidator(
        regex=r"^\d{5}$",
        message="Please enter a valid 5 digit zip code"
    )
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    home_address = models.CharField(max_length=255, blank=True)
    home_zip = models.CharField(
        validators=[zip_regex, ], max_length=5, blank=True
    )
    work_address = models.CharField(max_length=255, blank=True)
    work_zip = models.CharField(
        validators=[zip_regex, ], max_length=5, blank=True
    )
    phone_number = models.CharField(
        validators=[phone_regex, ], max_length=15,blank=True
    )

    phone_validated = models.BooleanField(default=False)
    #hangouts = models.ForeignKey(Hangout)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    objects = PlayerManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    def get_slug_field(self):
        return self.username

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def __unicode__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_phone_validated(self):
        return self.phone_validated

    @property
    def is_email_verified(self):
        return self.email_verified

    @is_phone_validated.setter
    def is_phone_validated(self, value):
        self.is_phone_validated = value

    @models.permalink
    def get_absolute_url(self):
        return ("players:detail", (), {"slug": self.username})