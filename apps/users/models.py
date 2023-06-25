from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.utils import IntegrityError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import exceptions


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, email, password, directions, month):
        if username is None:
            raise TypeError('Users should have username')
        if email is None:
            raise TypeError('Users should have email')
        user = self.model(username=username,
                          email=self.normalize_email(email), directions=directions, month=month)
        user.set_password(password)
        datas = (username, email)
        for data in datas:
            try:
                user.save()
            except IntegrityError:
                raise exceptions.ValidationError(f'This {data} is not available, please write another one')
        return user

    def create_superuser(self, username, email, password, directions, month):
        if password is None:
            raise TypeError('Password should not be none')
        user = self.create_user(username, email, password, directions, month)
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    DIRECTION_CHOICES = (
        ('Backend', 'Backend'),
        ('Frontend', 'Frontend'),
        ('UX/UI', 'UX/UI'),
        ('Android', 'Android'),
        ('IOS', 'IOS')
    )

    MONTH_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7')
    )

    email = models.EmailField(max_length=255, unique=True, db_index=True)
    username = models.CharField(max_length=255, unique=True, db_index=True)
    directions = models.CharField(choices=DIRECTION_CHOICES, max_length=255)
    month = models.CharField(choices=MONTH_CHOICES, max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False, help_text='Email activated')
    is_staff = models.BooleanField(default=False, help_text='Работник')
    is_superuser = models.BooleanField(default=False, help_text='админ')
    is_mentor = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'directions', 'month']
    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }