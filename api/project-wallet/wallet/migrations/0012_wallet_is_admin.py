# Generated by Django 4.2.5 on 2023-12-16 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0011_wallet_priv_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]