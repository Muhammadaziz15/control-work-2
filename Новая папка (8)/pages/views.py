import logging
import smtplib

from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render

from config.models import CompanyInfo

from .forms import ContactForm
from .models import ContactRequest, Service

logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'pages/home.html', {
        'company': CompanyInfo.objects.first(),
        'services': Service.objects.order_by('pk')[:3],
    })


def about(request):
    return render(request, 'pages/about.html', {
        'company': CompanyInfo.objects.first(),
    })


def services(request):
    return render(request, 'pages/services.html', {
        'services': Service.objects.order_by('pk'),
    })


def contact(request):
    company = CompanyInfo.objects.first()
    form = ContactForm(request.POST if request.method == 'POST' else None)

    if request.method == 'POST' and form.is_valid():
        if company is None:
            form.add_error(None, 'Сначала добавьте информацию о компании в панели администратора.')
        else:
            data = form.cleaned_data
            contact_request = ContactRequest.objects.create(
                name=data['name'],
                email=data['email'],
                phone=data['phone'],
                message=data['message'],
            )

            if settings.EMAIL_HOST:
                email = EmailMessage(
                    subject=f'Заявка с сайта: {contact_request.name}',
                    body=(
                        f'Имя: {contact_request.name}\n'
                        f'Email: {contact_request.email}\n'
                        f'Телефон: {contact_request.phone or "не указан"}\n\n'
                        f'Сообщение:\n{contact_request.message}'
                    ),
                    to=[company.email],
                    reply_to=[contact_request.email],
                )
                try:
                    sent = email.send(fail_silently=False)
                except (OSError, smtplib.SMTPException):
                    logger.exception('Could not send contact request email.')
                    messages.warning(
                        request,
                        'Заявка сохранена, но уведомление по email не отправлено. '
                        'Свяжитесь с нами по контактам ниже.',
                    )
                else:
                    if sent == 1:
                        messages.success(request, 'Спасибо! Сообщение отправлено.')
                    else:
                        logger.error('Email backend did not send contact request %s.', contact_request.pk)
                        messages.warning(
                            request,
                            'Заявка сохранена, но уведомление по email не отправлено. '
                            'Свяжитесь с нами по контактам ниже.',
                        )
            else:
                messages.success(
                    request,
                    'Спасибо! Заявка сохранена. Мы свяжемся с вами по указанным контактам.',
                )
            return redirect('pages:contact')

    return render(request, 'pages/contact.html', {
        'company': company,
        'form': form,
    })
