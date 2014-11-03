from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator
from localflavor.us.models import USPostalCodeField
from localflavor.us.models import PhoneNumberField
from localflavor.us.models import USStateField
#need to import models.py from the hangouts app eventually
from django import template

register = template.Library()

# Create your models here.
class PlayerManager(BaseUserManager):

    def live(self):
        return self.model.objects.filter(is_active=True)

"""
    def create_player(
        self,
        email,
        username,
        first_name='',
        last_name='',
        home_address='',
        state='',
        home_zip='',
        work_address='',
        work_zip='',
        phone_number='',
        password=None
    ):

        player = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            home_address=home_address,
            state=state,
            home_zip=home_zip,
            work_address=work_address,
            work_zip=work_zip,
            phone_number=phone_number,
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
        state='',
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
            state=state,
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

"""
class Player(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=255,
        verbose_name='Email address',
    )
    username = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='User name',
    )

    first_name = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="First name"
    )

    last_name = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Last name"
    )

    state = USStateField(blank=True, verbose_name="State")

    home_address = models.CharField(
        max_length=255, blank=True,
        verbose_name="Home address"
    )
    home_zip = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="Home zipcode"
    )

    work_address = models.CharField(
        max_length=255, blank=True,
        verbose_name="Work address"
    )

    work_zip = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="Work zipcode"
    )

    phone_number = PhoneNumberField(blank=True, verbose_name="Phone number")

    phone_validated = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)

    #hotspots = models.ForeignKey(Hotspot)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date joined"
    )

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

    @is_email_verified.setter
    def is_email_verified(self, value):
        self.email_verified = value

    @is_phone_validated.setter
    def is_phone_validated(self, value):
        self.phone_validated = value

    @models.permalink
    def get_absolute_url(self):
        return ("players:detail", (), {"slug": self.username})
