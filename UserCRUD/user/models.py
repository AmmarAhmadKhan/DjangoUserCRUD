from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class Role:
    ADMIN = "Admin"
    STAFF = "Staff"


def pakistan_mobile_validator(value):
    validator = RegexValidator(
        regex="^((\+92)?(0092)?(92)?(0)?)(3)([0-9]{9})$",
        message=_("Mobile Number is Invalid"),
        code="invalid_mobile",
    )
    return validator(value)


class Organization(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    _roles = Role()
    username = models.CharField(
        max_length=255, null=False, blank=False, unique=True
    )
    full_name = models.CharField(
        max_length=255, blank=True, null=True
    )
    email = models.EmailField(
        max_length=100, blank=True, null=True
    )
    mobile_number = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        validators=[pakistan_mobile_validator]
    )
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     related_name='users', null=True, blank=True)

    # objects = CustomUserManager()


CustomUser._meta.get_field('groups').remote_field.related_name = 'custom_user_groups'
CustomUser._meta.get_field('user_permissions').remote_field.related_name = 'custom_user_permissions'


class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50)
