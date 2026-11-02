from django.db import migrations


def replace_demo_phone_country_code(apps, schema_editor):
    CompanyInfo = apps.get_model('config', 'CompanyInfo')
    database = schema_editor.connection.alias

    for company in CompanyInfo.objects.using(database).all():
        changed = False
        if company.phone.startswith('+7'):
            company.phone = '+996' + company.phone[2:]
            changed = True
        if company.whatsapp_url.startswith('https://wa.me/7'):
            company.whatsapp_url = (
                'https://wa.me/996' + company.whatsapp_url[len('https://wa.me/7'):]
            )
            changed = True
        if changed:
            company.save(
                using=database,
                update_fields=('phone', 'whatsapp_url'),
            )


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0002_companyinfo_telegram_url_companyinfo_whatsapp_url_and_more'),
    ]

    operations = [
        migrations.RunPython(replace_demo_phone_country_code, migrations.RunPython.noop),
    ]
