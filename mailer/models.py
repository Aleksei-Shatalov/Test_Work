# coding: utf-8
from __future__ import unicode_literals
from django.db import models


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Mailing(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Запланирована'),
        ('sent', 'Отправлена'),
        ('failed', 'Ошибка'),
    )

    subject = models.CharField(max_length=255)
    body = models.TextField()
    subscribers = models.ManyToManyField(Subscriber, related_name='mailings', blank=True)
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

