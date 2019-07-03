from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MaxValueValidator

from accounts.models import User

User = get_user_model()


class Challenge(models.Model):
    DIFFICULTY = [

    ]

    CATEGORY = [
        ('GS', 'General Skills'),
        ('CR', 'Crypto'),
        ('ST', 'Stego'),
        ('BE', 'Binary Exploitation'),
        ('WE', 'Web Exploitation'),
        ('FR', 'Forensics'),
        ('RV', 'Reversing')
    ]

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='labs_author')
    title = models.CharField(max_length=40)
    description = models.TextField()
    category = models.CharField(max_length=2, choices=CATEGORY, default='GS')
    created = models.DateTimeField(default=timezone.now)
    download_link = models.URLField()
    zip_pass = models.CharField(max_length=40)
    sha256 = models.CharField(max_length=64)
    points = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(50)])
    solvers = models.ManyToManyField(User, related_name='chg_solved')
    rate_pro = models.PositiveSmallIntegerField(default=0, editable=False)
    rate_sucks = models.PositiveSmallIntegerField(default=0, editable=False)
    flag = models.CharField(max_length=40, blank=True)

    def __str__(self):
        return f'"{self.title}" by {self.author.username}'

    def check_flag(self, user_flag, user):
        if user_flag.upper() == self.flag.upper():
            self.solvers.add(user)
            user.profile.points += int(self.points)
            user.profile.update_rank()
            user.profile.save()
            return True
        else:
            return False
