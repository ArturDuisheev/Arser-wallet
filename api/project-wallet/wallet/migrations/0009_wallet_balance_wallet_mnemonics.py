# Generated by Django 4.2.5 on 2023-11-19 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0008_alter_payment_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='balance',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wallet',
            name='mnemonics',
            field=models.TextField(blank=True, null=True),
        ),
    ]
