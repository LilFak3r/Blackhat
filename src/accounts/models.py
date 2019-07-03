from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager
)
from django.core.validators import RegexValidator, MaxValueValidator
from django.utils import timezone
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

USERNAME_REGEX = "^[a-zA-Z0-9]*$"


class UserManager(BaseUserManager):
    def _create_user(
        self, email, username, password, is_staff, is_superuser, is_active, **extra_fields,
    ):
        if not email:
            raise ValueError("Email required")
        if not username:
            raise ValueError("Username required")
        if not password:
            raise ValueError("Password required")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            is_active=True,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        return self._create_user(
            email, username, password, True, False, False, **extra_fields
        )

    def create_superuser(self, email, username, password, **extra_fields):
        return self._create_user(
            email, username, password, True, True, True, **extra_fields
        )


class User(AbstractBaseUser):
    email = models.EmailField(
        max_length=40,
        unique=True,
        error_messages={"unique": "A user with that email already exists"},
    )
    username = models.CharField(
        max_length=40,
        validators=[
            RegexValidator(
                regex=USERNAME_REGEX,
                message="Username may only contain letters and numbers"
            )
        ], unique=True,
        error_messages={"unique": "A user with that username already exists"}
    )
    country = models.CharField(max_length=2, default="UA")
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class UserProfile(models.Model):
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    rankStr = models.CharField(max_length=40, default="Newbie")
    rankPercentage = models.PositiveSmallIntegerField(
        default=0, validators=[MaxValueValidator(100)], verbose_name="Rank %"
    )
    points = models.PositiveSmallIntegerField(default="0")

    def __str__(self):
        return f"{self.user.username} profile"

    def __set_rank(self, points):
        if points <= 99:
            return 'Newbie'
        elif points >= 100 and points <= 199:
            return 'Script Kiddie'
        elif points >= 200 and points <= 249:
            return 'Hacker'
        elif points >= 250 and points <= 349:
            return 'Pro Hacker'
        elif points >= 350 and points <= 399:
            return 'Elite Hacker'
        elif points >= 400 and points <= 449:
            return 'Guru'
        elif points >= 450 and points <= 500:
            return 'Omniscient'

    def update_rank(self):
        self.rankStr = self.__set_rank(int(self.points))
        return self.rankStr


@receiver(post_save, sender=User)
def create_profile_challenges(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_userprofile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=User)
def update(sender, instance, **kwargs):
    instance.profile.update_rank()
