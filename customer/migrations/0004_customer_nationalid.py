# Generated by Django 4.2.2 on 2023-08-26 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_customer_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='nationalid',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]