from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Room(models.Model):
    name = models.TextField()
    label = models.SlugField(unique=True)

    def __unicode__(self):
        return self.label


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages')
    author = models.ForeignKey(
        User,
        related_name='message_author',
        blank=True)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    def __unicode__(self):
        return '[{timestamp}] {author}: {message}'.format(**self.as_dict())

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%b %-d %H:%M')

    def as_dict(self):
        return {
            'author': self.author.username,
            'message': self.message,
            'timestamp': self.formatted_timestamp}
