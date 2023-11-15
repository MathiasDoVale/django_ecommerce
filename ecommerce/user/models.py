from django.db import models  # noqa: F401
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

# Create your models here.

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """
    Stores a user (whether administrator or client).

    """
    username = None
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(max_length=30, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Address(models.Model):
    country = CountryField(blank=True)
    state_province = models.CharField(max_length=80, blank=True)
    postal_zip_code = models.CharField(max_length=12, blank=True)
    city = models.CharField(max_length=80, blank=True)
    street_address = models.CharField(max_length=80, blank=True)
    building_number = models.CharField(max_length=12, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class ShippingAddress(Address):

    """
    Stores the address of a user.

    """
    user = models.ManyToManyField(CustomUser, related_name='shipping_addresses')  # noqa: E501


class BillingAddress(Address):
    """
    Stores the billing address of a user.

    """
    user = models.ManyToManyField(CustomUser, related_name='billing_addresses')
    tax_id = models.CharField(max_length=30, blank=True)


"""
Purchase History: A record of the user's previous purchases, including details like purchased products, purchase date, and order status.
Wish List: If your platform allows users to create and manage lists of desired products.
User Role: Defines the user's level of access or permissions (e.g., admin, customer, employee, etc.).
Account Status: Can indicate if the account is active, locked, or suspended.
Profile Picture or Avatar: To allow users to personalize their profiles.
Notification and Communication Preferences: Settings for notification and communication preferences."""  # noqa: E501
""" Verification Code: For implementing email verification or two-factor authentication.
Password Reset Token: If you allow users to reset their passwords.
Security Questions/Answers: Additional security measures, like security questions and answers. """  # noqa: E501
