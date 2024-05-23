from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        max_length=1024,
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='following',
                             on_delete=models.CASCADE)
    followed_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                      related_name='followed_by',
                                      on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'followed_user')


class UserBlock(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='blocking', on_delete=models.CASCADE)
    blocked_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     related_name='blocked_by',
                                     on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'blocked_user')
