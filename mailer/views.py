# coding: utf-8
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Mailing, Subscriber, EmailOpenTracking
from .forms import MailingForm
from .tasks import send_newsletter
from django.utils import timezone
import uuid
import logging

logger = logging.getLogger(__name__)

def create_mailing(request):
    if request.method == 'POST':
        form = MailingForm(request.POST)
        if form.is_valid():
            mailing = form.save(commit=False)
            mailing.created_at = timezone.now()
            mailing.save()
            form.save_m2m()
            send_newsletter.apply_async((mailing.id,), eta=mailing.scheduled_time)
            return JsonResponse({'status': 'success', 'message': 'Рассылка успешно создана и будет отправлена позже.'})
        print(form.errors)  # Выведем ошибки формы в консоль
        return JsonResponse({'status': 'error', 'message': 'Ошибка при создании рассылки.', 'errors': form.errors})

    form = MailingForm()

    # Преобразуем scheduled_time в нужный формат
    if form.instance.scheduled_time:
        scheduled_time = form.instance.scheduled_time.strftime('%Y-%m-%dT%H:%M')
    else:
        scheduled_time = timezone.now().strftime('%Y-%m-%dT%H:%M')

    return render(request, 'mailer/create_mailing.html', {
        'form': form,
        'scheduled_time': scheduled_time,
    })


def mailing_list(request):
    mailings = Mailing.objects.all()
    return render(request, 'mailer/mailing_list.html', {'mailings': mailings})


def mailing_detail(request, mailing_id):
    try:
        mailing = Mailing.objects.get(id=mailing_id)
    except Mailing.DoesNotExist:
        return render(request, 'mailer/error.html', {'message': 'Рассылка не найдена.'})
    return render(request, 'mailer/mailing_detail.html', {'mailing': mailing})


def track_email_open(request, mailing_id, tracking_token):
    try:
        mailing = get_object_or_404(Mailing, id=mailing_id)

        if isinstance(tracking_token, str):
            try:
                tracking_token = uuid.UUID(tracking_token)
            except ValueError:
                logger.error(u"Invalid tracking_token: {}".format(tracking_token))
                return HttpResponse(u"Invalid tracking_token", status=400)

        subscriber = get_object_or_404(Subscriber, tracking_token=tracking_token)

        logger.info(u"Email opened by {} for mailing {}".format(subscriber.email, mailing.subject))

        EmailOpenTracking.objects.create(
            mailing=mailing,
            subscriber=subscriber,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT'),
        )

    except Mailing.DoesNotExist:
        logger.error(u"Mailing with id={} not found.".format(mailing_id))
        return HttpResponse(u"Mailing not found", status=404)

    except Subscriber.DoesNotExist:
        logger.error(u"Subscriber with tracking_token={} not found.".format(tracking_token))
        return HttpResponse(u"Subscriber not found", status=404)

    except Exception as e:
        logger.error(u"Error tracking email open: {}".format(str(e)))
        return HttpResponse(u"Error tracking", status=500)

    pixel = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
    return HttpResponse(pixel, content_type='image/gif')