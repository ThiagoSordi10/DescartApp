from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.conf import settings
from datetime import datetime
from .models_managers import (WithoutExcludedManager, WithExcludedManager)


User = settings.AUTH_USER_MODEL
# https://www.codingforentrepreneurs.com/blog/how-to-create-a-custom-django-user-model

class BaseModel(models.Model):

    created = models.DateTimeField(db_index=True, auto_now_add=True)
    updated = models.DateTimeField(db_index=True, auto_now=True)

    class Meta:
        abstract = True


class LogicDeletable(models.Model):
    u"""
    Classe que fornece funcionalidade pra delete lógico de um modelo.

    Pode armazenar quem deletou e quando, também pode reativar o modelo.
    Já possui managers pra filtrar excluídos e não excluídos.
    """

    excluded = models.BooleanField(default=False, db_index=True)
    excluded_by = models.ForeignKey(User, related_name='%(class)s_excluded_by', null=True, blank=True, on_delete=models.SET_NULL)
    excluded_at = models.DateTimeField(null=True, blank=True)

    objects = WithExcludedManager()
    with_excluded = WithExcludedManager()

    def delete(self, using=None):
        self.excluded = True
        self.excluded_at = datetime.now()
        self.save()

    def logic_delete(self, user, using=None):
        self.excluded_by = user
        self.save()
        self.delete(using)

    def reativar(self):
        self.excluded = False
        self.excluded_by = None
        self.excluded_at = None
        self.save()

    def hard_delete(self, using=None):
        # Força a exclusão dos itens diretamente no modelo
        super().delete()

    class Meta:
        abstract = True

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_superuser(self):
        "Is the user a superuser member?"
        return self.admin and self.staff


class Person(BaseModel, LogicDeletable):

    name = models.CharField(max_length=255)
    rg = models.CharField(max_length=14, db_index=True)
    cpf = models.CharField(max_length=14, unique=True)
    birth_date = models.DateField()
    photo = models.ImageField(blank=True)
    user = models.OneToOneField(User,
                                null=True,
                                blank=True,
                                related_name="person",
                                on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        names = self.name.split()
        self.user.first_name = names[0]
        self.user.last_name = " ".join(names[1:])
        self.user.save()

    def __str__(self):
        return self.name


class Company(BaseModel, LogicDeletable):

    trade = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=14)
    photo = models.ImageField(blank=True)
    user = models.OneToOneField(User,
                                null=True,
                                blank=True,
                                related_name="company",
                                on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.user.first_name = self.nome
        self.user.save()

    def __str__(self):
        return self.trade

class Collector(BaseModel, LogicDeletable):

    user = models.OneToOneField(User,
                                null=True,
                                blank=True,
                                related_name="collector",
                                on_delete=models.CASCADE)

class Discarder(BaseModel, LogicDeletable):

    user = models.OneToOneField(User,
                                null=True,
                                blank=True,
                                related_name="discarder",
                                on_delete=models.CASCADE)