# Generated by Django 5.1.6 on 2025-03-12 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.BigIntegerField(primary_key=True, serialize=False, unique=True, verbose_name='Telegram ID'),
        ),
    ]
