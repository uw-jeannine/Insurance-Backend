# Generated by Django 4.2.2 on 2023-08-30 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
        ('insurance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='applypolicyvehicle',
            name='applyid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insurance.policy'),
        ),
        migrations.AddField(
            model_name='applypolicyvehicle',
            name='customerid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer'),
        ),
        migrations.AddField(
            model_name='applypolicyagriculture',
            name='appliedid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insurance.policy'),
        ),
        migrations.AddField(
            model_name='applypolicyagriculture',
            name='customerid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer'),
        ),
    ]
