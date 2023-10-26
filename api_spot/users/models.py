from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from phonenumber_field import modelfields

from users.validators import NamesValidator, validate_birth_day


class MyUserManager(BaseUserManager):
    """
    Кастомный менеджер для модели User
    """
    def _create_user(self, email, password, **extra_fields):
        """
        Создает и сохраняет юзера с почтой, телефоном, и паролем
        """
        if not email:
            raise ValueError('Электронная почта обязательна')
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        """
        Создает юзера
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            email,
            password,
            **extra_fields
        )

    def create_superuser(self, email, password, **extra_fields):
        """
        Создает суперюзера
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(
            email,
            password,
            **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(
        'Имя',
        max_length=150,
        validators=(NamesValidator(),)
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        validators=(NamesValidator(),)
    )
    email = models.EmailField(
        'Электронная почта',
        unique=True,
        error_messages={
            'unique': 'Этот адрес электронной почты уже зарегистрован.'
        }
    )
    phone = modelfields.PhoneNumberField(
        'Телефон',
        region='RU',
        unique=True,
        blank=True,
        null=True,
    )
    birth_date = models.DateField(
        'Дата рождения',
        blank=True,
        null=True,
        validators=[validate_birth_day]
    )
    is_staff = models.BooleanField(
        'Стафф статус',
        default=False,
    )
    is_active = models.BooleanField(
        'Статус - активный',
        default=False,
    )
    date_joined = models.DateTimeField(
        'Дата регистрации', default=timezone.now
    )
    occupation = models.CharField(
        'Род деятельности',
        max_length=128,
        blank=True,
        default='',
    )

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)


class Avatar(models.Model):
    user = models.OneToOneField(
        User,
        related_name='avatar',
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        'Аватар',
        blank=True,
        null=True,
        upload_to='images/users/',
    )

    class Meta:
        verbose_name = 'Аватар'
        verbose_name_plural = 'Аватарки'
        ordering = ('user',)

    def __str__(self) -> str:
        return self.user.first_name
