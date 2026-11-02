from django.db import models


class Service(models.Model):
    name = models.CharField('Название услуги', max_length=200)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    image = models.ImageField('Изображение', upload_to='services/', blank=True)

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class ContactRequest(models.Model):
    name = models.CharField('Имя', max_length=100)
    email = models.EmailField('Электронная почта')
    phone = models.CharField('Телефон', max_length=30, blank=True)
    message = models.TextField('Сообщение')
    created_at = models.DateTimeField('Дата получения', auto_now_add=True)
    is_processed = models.BooleanField('Обработано', default=False)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.name} — {self.created_at:%d.%m.%Y %H:%M}'
