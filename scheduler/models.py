import uuid

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _


class ScheduledPost(models.Model):
    user = models.ForeignKey(User)
    status = models.TextField()
    service = models.CharField(max_length=20, choices=(
        ("facebook", _("Facebook")),
        ("twitter", _("Twitter")),
    ))
    scheduled_datetime = models.DateTimeField()
    is_posted = models.BooleanField(default=False)

    def __str__(self):
        return "{0}: {1}... to {2} at {3}".format(
            self.user.username, self.status[:10],
            self.service, self.scheduled_datetime)


class AuthenticationToken(models.Model):
    user  = models.ForeignKey(User)
    token = models.TextField(unique=True)

    def __str__(self):
        return self.user.username


def create_user_auth_token(sender, **kwargs):
    if not kwargs.get("created"):
        return None
    token = str(uuid.uuid4()).replace('-', '')
    AuthenticationToken.objects.create(
        user=kwargs["instance"],
        token=token)
post_save.connect(create_user_auth_token, sender=User)