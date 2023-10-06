# Generated by Django 4.2.5 on 2023-10-06 05:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано в: ')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено в: ')),
                ('amount', models.DecimalField(decimal_places=6, max_digits=10, verbose_name='Сумма')),
                ('network', models.CharField(choices=[('USDT', 'Usdt'), ('BTC', 'Btc'), ('MONERO', 'Monero'), ('TON', 'Ton')], max_length=10)),
                ('currency', models.CharField(choices=[('USD', 'Usd'), ('EUR', 'Eur'), ('RUB', 'Rub')], max_length=10)),
                ('order_id', models.IntegerField(verbose_name='ID заказа')),
                ('address', models.CharField(max_length=200, verbose_name='Адрес')),
                ('url_callback', models.CharField(max_length=200, verbose_name='Ссылка')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]