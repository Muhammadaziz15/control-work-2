from django.contrib import admin
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from config.models import CompanyInfo

from .models import ContactRequest, Service


class PublicPagesTests(TestCase):
    def setUp(self):
        self.company = CompanyInfo.objects.first()
        self.company.company_name = 'DigitalHub Test'
        self.company.description = 'Описание компании'
        self.company.phone = '+996 700 000-000'
        self.company.email = 'hello@example.com'
        self.company.address = 'Тестовый адрес'
        self.company.save()

        self.service = Service.objects.order_by('pk').first()
        self.service.name = 'Разработка сайта'
        self.service.description = 'Создание адаптивного сайта'
        self.service.price = '25000.00'
        self.service.save()

    def test_all_navigation_pages_load(self):
        for page_name in ('home', 'about', 'services', 'contact'):
            with self.subTest(page=page_name):
                response = self.client.get(reverse(f'pages:{page_name}'))
                self.assertEqual(response.status_code, 200)

    def test_navigation_links_have_working_named_routes(self):
        response = self.client.get(reverse('pages:home'))
        for page_name in ('home', 'about', 'services', 'contact'):
            self.assertContains(response, reverse(f'pages:{page_name}'))
        self.assertContains(response, '/static/css/style.css')
        self.assertContains(response, '/static/js/main.js')
        self.assertContains(response, '/static/images/hero-illustration.png')
        self.assertContains(response, '/static/images/digitalhub-logo.png')

    def test_company_and_services_are_rendered_from_database(self):
        home_response = self.client.get(reverse('pages:home'))
        self.assertContains(home_response, self.company.company_name)
        self.assertContains(home_response, self.service.name)

        services_response = self.client.get(reverse('pages:services'))
        self.assertContains(services_response, self.service.description)
        self.assertContains(services_response, 'сом')
        self.assertContains(services_response, '/static/images/service1.png')

        contact_response = self.client.get(reverse('pages:contact'))
        self.assertContains(contact_response, self.company.email)
        self.assertContains(contact_response, 'name="csrfmiddlewaretoken"')

    def test_about_page_uses_supplied_template_illustration(self):
        response = self.client.get(reverse('pages:about'))
        self.assertContains(response, '/static/images/about-illustration.png')

    def test_models_are_registered_in_admin(self):
        self.assertIn(CompanyInfo, admin.site._registry)
        self.assertIn(Service, admin.site._registry)
        self.assertIn(ContactRequest, admin.site._registry)

    def test_second_service_uses_second_static_illustration(self):
        Service.objects.create(
            name='Мобильное приложение',
            description='Адаптация для смартфонов',
            price='30000.00',
        )
        Service.objects.create(
            name='Продвижение',
            description='Аналитика и развитие проекта',
            price='15000.00',
        )

        services_response = self.client.get(reverse('pages:services'))

        self.assertContains(services_response, '/static/images/service1.png')
        self.assertContains(services_response, '/static/images/service2.png')
        self.assertContains(services_response, '/static/images/service3.png')

    @override_settings(
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
        EMAIL_HOST='smtp.example.com',
    )
    def test_contact_form_sends_message_to_company_email(self):
        response = self.client.post(reverse('pages:contact'), {
            'name': 'Тестовый клиент',
            'email': 'client@example.com',
            'phone': '+996 700 000-000',
            'message': 'Нужен сайт для компании.',
        })

        self.assertRedirects(response, reverse('pages:contact'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.company.email])
        self.assertEqual(mail.outbox[0].reply_to, ['client@example.com'])
        self.assertEqual(ContactRequest.objects.count(), 1)
        self.assertEqual(ContactRequest.objects.get().email, 'client@example.com')

    def test_contact_form_saves_request_without_smtp_configuration(self):
        response = self.client.post(reverse('pages:contact'), {
            'name': 'Посетитель',
            'email': 'visitor@example.com',
            'phone': '',
            'message': 'Хочу узнать подробности.',
        })

        self.assertRedirects(response, reverse('pages:contact'))
        self.assertEqual(ContactRequest.objects.count(), 1)
        self.assertEqual(ContactRequest.objects.get().name, 'Посетитель')
