from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
import re
from django.conf import settings


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_field):
        " A function to handle creating a user. "
        email = self.normalize_email(email=email)
        email_regex = (
            "^[^@\s#$%*()&~`!\^]+@[^@\s#$%*()&~`!\^]+\.(com|net|org|gov|example)$" #noqa
        )
        valid = re.match(pattern=email_regex, string=email)
        if valid is None:
            raise ValueError("User must have a valid email address!")
        user = self.model(email=email, **extra_field)
        user.set_password(raw_password=password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        " A function to handle creating a superuser."

        user = self.create_user(email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = "email"  # Use email field for login

    objects = UserManager()


class Recipe(models.Model):
    " Recipe object."
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )  # A many - to - one relation

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        "Overriden DunDer method"
        return self.title
