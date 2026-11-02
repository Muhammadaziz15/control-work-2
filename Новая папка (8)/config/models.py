from django.db import models


class CompanyInfo(models.Model):
    company_name = models.CharField('Название компании', max_length=200)
    description = models.TextField('Описание')
    logo = models.ImageField('Логотип', upload_to='company/', blank=True)
    phone = models.CharField('Номер телефона', max_length=30)
    email = models.EmailField('Электронная почта')
    address = models.CharField('Адрес', max_length=255)
    instagram_url = models.URLField('Instagram', blank=True)
    facebook_url = models.URLField('Facebook', blank=True)
    linkedin_url = models.URLField('LinkedIn', blank=True)
    telegram_url = models.URLField('Telegram', blank=True)
    whatsapp_url = models.URLField('WhatsApp', blank=True)
    youtube_url = models.URLField('YouTube', blank=True)

    class Meta:
        verbose_name = 'Информация о компании'
        verbose_name_plural = 'Информация о компании'
        ordering = ('id',)

    def __str__(self):
        return self.company_name
