from django.db import models

# Create your models here.
#Should extends from User default class in django, adding new fields.

""" User ID: A unique reference number to identify the user in your system. This number is typically generated automatically.
Registration Date: The date when the user account was created.
Username: A unique field used as the login identifier.
Email Address: For communication and password recovery.
Password: Stores the user's password securely (use hashing and salting techniques).
Shipping Address: Fields for the user's shipping address, including street, city, postal/ZIP code, state/province, country, etc.
Billing Address: If different from the shipping address, fields for the billing address.
Phone Number: May be useful for communication and two-factor authentication.
Payment Methods: If you allow users to store credit card or other payment method information.
Purchase History: A record of the user's previous purchases, including details like purchased products, purchase date, and order status.
Wish List: If your platform allows users to create and manage lists of desired products.
User Role: Defines the user's level of access or permissions (e.g., admin, customer, employee, etc.).
Account Status: Can indicate if the account is active, locked, or suspended.
Profile Picture or Avatar: To allow users to personalize their profiles.
Notification and Communication Preferences: Settings for notification and communication preferences.
Verification Code: For implementing email verification or two-factor authentication.
Password Reset Token: If you allow users to reset their passwords.
Security Questions/Answers: Additional security measures, like security questions and answers. """

