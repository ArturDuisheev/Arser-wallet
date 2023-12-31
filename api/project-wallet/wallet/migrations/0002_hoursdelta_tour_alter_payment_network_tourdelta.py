# Generated by Django 4.2.5 on 2023-10-14 15:20

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HoursDelta',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано в: ')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено в: ')),
                ('hour_start', models.IntegerField(verbose_name='Начальная час')),
                ('hour_end', models.IntegerField(verbose_name='Конечная час')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано в: ')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено в: ')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='payment',
            name='network',
            field=models.CharField(choices=[('BTC', 'Btc'), ('MONERO', 'Monero'), ('TON', 'Ton'), ('TRON', 'Tron')], max_length=10),
        ),
        migrations.CreateModel(
            name='TourDelta',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано в: ')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено в: ')),
                ('price', models.DecimalField(decimal_places=6, max_digits=10, verbose_name='Цена')),
                ('currency', models.CharField(choices=[('USD', 'Usd'), ('EUR', 'Eur'), ('RUB', 'Rub')], max_length=10)),
                ('hours_delta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallet.hoursdelta', verbose_name='Длительность')),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallet.tour', verbose_name='Тур')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
