# coding: utf-8
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Mailing, Subscriber
from .forms import MailingForm
from .tasks import send_newsletter
from django.utils import timezone


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


