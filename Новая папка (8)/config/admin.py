from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import CompanyInfo


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'phone', 'email')
    search_fields = ('company_name', 'email', 'address')
    fieldsets = (
        ('Основная информация', {
            'fields': ('company_name', 'description', 'logo'),
        }),
        ('Контакты', {
            'fields': ('phone', 'email', 'address'),
        }),
        ('Социальные сети', {
            'fields': (
                'instagram_url',
                'facebook_url',
                'linkedin_url',
                'telegram_url',
                'whatsapp_url',
                'youtube_url',
            ),
        }),
    )
