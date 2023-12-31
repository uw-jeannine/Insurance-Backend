# Generated by Django 4.2.2 on 2023-08-30 12:13

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
            name='ApplyPolicyAgriculture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policy_status', models.CharField(blank=True, max_length=255, null=True)),
                ('crop_type', models.CharField(blank=True, max_length=255, null=True)),
                ('insurance_type', models.CharField(blank=True, max_length=255, null=True)),
                ('plot_size', models.CharField(blank=True, max_length=255, null=True)),
                ('crop_name', models.CharField(blank=True, max_length=255, null=True)),
                ('planting_date', models.DateField(blank=True, null=True)),
                ('harvest_date', models.DateField(blank=True, null=True)),
                ('soiltype', models.CharField(blank=True, max_length=255, null=True)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('tracking_number', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ApplyPolicyMedical',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policy_number', models.CharField(blank=True, max_length=255, null=True)),
                ('policy_holder_name', models.CharField(blank=True, max_length=255, null=True)),
                ('policy_start_date', models.DateField(blank=True, null=True)),
                ('policy_end_date', models.DateField(blank=True, null=True)),
                ('premium_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('deductible', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('coverage_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('policy_status', models.CharField(blank=True, max_length=255, null=True)),
                ('insured_person_name', models.CharField(blank=True, max_length=255, null=True)),
                ('insured_person_age', models.CharField(blank=True, max_length=255, null=True)),
                ('insured_person_gender', models.CharField(blank=True, max_length=255, null=True)),
                ('insured_person_address', models.CharField(blank=True, max_length=255, null=True)),
                ('tracking_number', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ApplyPolicyProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policy_number', models.CharField(blank=True, max_length=255, null=True)),
                ('policy_holder_name', models.CharField(blank=True, max_length=255, null=True)),
                ('policy_start_date', models.DateField(blank=True, null=True)),
                ('policy_end_date', models.DateField(blank=True, null=True)),
                ('premium_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('coverage_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('policy_status', models.CharField(blank=True, max_length=255, null=True)),
                ('property_address', models.CharField(blank=True, max_length=255, null=True)),
                ('property_type', models.CharField(blank=True, max_length=255, null=True)),
                ('construction_type', models.CharField(blank=True, max_length=255, null=True)),
                ('property_value', models.CharField(blank=True, max_length=255, null=True)),
                ('insurance_coverage', models.CharField(blank=True, max_length=255, null=True)),
                ('tracking_number', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ApplyPolicyVehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marque', models.CharField(blank=True, max_length=255, null=True)),
                ('platenumnber', models.CharField(blank=True, max_length=255, null=True)),
                ('yearofmanufacture', models.CharField(blank=True, max_length=255, null=True)),
                ('insuredvalue', models.CharField(blank=True, max_length=255, null=True)),
                ('territoriallimit', models.CharField(blank=True, max_length=255, null=True)),
                ('model', models.CharField(blank=True, max_length=255, null=True)),
                ('numberofchasis', models.CharField(blank=True, max_length=255, null=True)),
                ('seatcapacity', models.CharField(blank=True, max_length=255, null=True)),
                ('occupantcover', models.CharField(blank=True, max_length=255, null=True)),
                ('policystatus', models.CharField(blank=True, max_length=255, null=True)),
                ('tracking_number', models.CharField(blank=True, max_length=255, null=True)),
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
                ('coverage_amount', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pic/Customer/')),
                ('address', models.CharField(max_length=40)),
                ('mobile', models.CharField(max_length=20)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('nationalid', models.CharField(blank=True, max_length=16, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
