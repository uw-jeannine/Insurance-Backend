# Generated by Django 4.2.3 on 2023-08-17 11:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplyPolicyVehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marque', models.CharField(blank=True, max_length=255, null=True)),
                ('platenumnber', models.CharField(blank=True, max_length=255, null=True)),
                ('yearofmanufacture', models.CharField(blank=True, max_length=255, null=True)),
                ('insuredvalue', models.CharField(blank=True, max_length=255, null=True)),
                ('territoriallimit', models.CharField(blank=True, max_length=255, null=True)),
                ('deductible', models.CharField(blank=True, max_length=255, null=True)),
                ('model', models.CharField(blank=True, max_length=255, null=True)),
                ('numberofchasis', models.CharField(blank=True, max_length=255, null=True)),
                ('seatcapacity', models.CharField(blank=True, max_length=255, null=True)),
                ('typeofvehicle', models.CharField(blank=True, max_length=255, null=True)),
                ('occupantcover', models.CharField(blank=True, max_length=255, null=True)),
                ('policystatus', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Submit_claim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('phonenumber', models.IntegerField()),
                ('policynumber', models.CharField(blank=True, max_length=255, null=True)),
                ('claim_type', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('dateofincident', models.DateField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('witnessinformation', models.CharField(blank=True, max_length=255, null=True)),
                ('vehicleproperty', models.CharField(blank=255, max_length=255, null=255)),
                ('policereport', models.FileField(upload_to='')),
                ('injuryinformation', models.CharField(blank=True, max_length=255, null=True)),
                ('uploadphotos', models.FileField(upload_to='')),
                ('additionalcomment', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pic/Customer/')),
                ('address', models.CharField(max_length=40)),
                ('mobile', models.CharField(max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
