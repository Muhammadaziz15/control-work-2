from django.contrib import admin

from .models import ContactRequest, Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')
    readonly_fields = ('name', 'email', 'phone', 'message', 'created_at')
    list_editable = ('is_processed',)
