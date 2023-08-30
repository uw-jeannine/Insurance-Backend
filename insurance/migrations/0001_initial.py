# Generated by Django 4.2.2 on 2023-08-30 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=30)),
                ('creation_date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policy_name', models.CharField(max_length=200)),
                ('type_of_vehicle', models.CharField(choices=[('person_goods_transport', 'Person & Goods Transport Cars'), ('minibus', 'Minibus & Minibus Carrying Goods'), ('motorcycle', 'Motorcycles'), ('bus', 'Buses'), ('truck', 'Trucks'), ('van', 'Van Vehicles'), ('driving_school', 'Driving School Vehicles'), ('trailer_semi_trailers', 'Trailer & Semi-Trailers'), ('tractor', 'Tractor'), ('Crop', 'Crop Insurance'), ('Forestry', 'Forestry Insurance'), ('Warehouse', 'Warehouse Receipt Insurance'), ('Equipment', 'Equipment Insurance')], max_length=255)),
                ('premium_amount', models.PositiveIntegerField()),
                ('deductible', models.PositiveIntegerField()),
                ('tenure', models.PositiveIntegerField()),
                ('creation_date', models.DateField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insurance.category')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=500)),
                ('admin_comment', models.CharField(default='Nothing', max_length=200)),
                ('asked_date', models.DateField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
            ],
        ),
        migrations.CreateModel(
            name='PolicyRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='Pending', max_length=100)),
                ('creation_date', models.DateField(auto_now=True)),
                ('Policy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insurance.policy')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
            ],
        ),
    ]
