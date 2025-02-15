# coding: utf-8
from celery import shared_task
from django.core.mail import send_mail
from .models import Mailing, Subscriber
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging
import os
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

@shared_task
def send_newsletter(mailing_id):
    try:
        mailing = Mailing.objects.get(id=mailing_id)
    except Mailing.DoesNotExist:
        logger.error("Mailing with ID {} not found.".format(mailing_id))
        return

    subscribers = mailing.subscribers.all()

    for subscriber in subscribers:
        html_message = render_to_string('mailer/newsletter_email.html', {
            'mailing': mailing,
            'subscriber': subscriber,
        })
        plain_message = strip_tags(html_message)

        try:
            send_mail(
                mailing.subject,
                plain_message,
                [os.getenv('EMAIL_HOST_USER')],
                [subscriber.email],
                fail_silently = False,
                html_message=html_message,
            )

        except Exception as e:
            logger.error("Error sending email to {}: {}".format(subscriber.email, str(e)))

    mailing.status = 'sent'
    mailing.save()


