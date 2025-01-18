# Generated by Django 5.1.4 on 2025-01-16 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0007_payments_status_alter_payments_amount"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="tg_chat_id",
            field=models.CharField(
                blank=True,
                help_text="Укажите телеграмм",
                max_length=50,
                null=True,
                verbose_name="telegram chat id",
            ),
        ),
    ]
