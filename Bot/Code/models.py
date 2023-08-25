from django.db import models

class Users(models.Model):
    telegram_id = models.IntegerField(unique=True)
    username = models.TextField(blank=True)
    nickname = models.TextField(blank=True)
    is_admin = models.BooleanField(default=True)
    admin_answered = models.BooleanField(default=False)
    answered_to = models.IntegerField(blank=True, default=0)
    telegram_id = models.IntegerField(default=0)


class Messages(models.Model):
    telegram_id = models.IntegerField()
    message = models.TextField(default=True)
    answered_message = models.TextField(blank=True)
    message_id = models.IntegerField(primary_key=True, default=0, blank=True)

