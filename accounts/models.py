from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from crep.models import Province, Municipality, Ward, Councilor
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.

class AccountManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_('Please provide a valid email address'))
    
    def create_user(self, first_name, last_name, username, email, password, **extra_fields):
        if email:
            email=self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_('An email address is required'))
        
        if not first_name:
            raise ValueError(_('First name is required'))
        if not last_name:
            raise ValueError(_('Last name is required'))
        
        user = self.model(email=email, username=username, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, email, username, password, **extra_fields):
        user = self.create_user(
            email=email, 
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=100, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=100, verbose_name=_('Last Name'))
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True, verbose_name=_('Email Address'))
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, blank=True)
    municipality = models.ForeignKey(Municipality, on_delete=models.SET_NULL, null=True, blank=True)
    Councilor = models.ForeignKey(Councilor, on_delete=models.SET_NULL, null=True, blank=True)
    ward = models.ForeignKey(Ward,  on_delete=models.SET_NULL, null=True, blank=True)
    section_or_area = models.CharField(max_length=100)
    
    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = AccountManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True
    
    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def tokens(self):
        refresh=RefreshToken.for_user(self)
        return {
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }

class OTP(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    pin = models.CharField(max_length=8, unique=True)

    def __str__(self):
        return f"{self.user.first_name}-passcode"