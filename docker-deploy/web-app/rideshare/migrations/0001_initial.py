# Generated by Django 4.2.9 on 2024-01-30 03:04

from django.db import migrations, models
import django.db.models.deletion
import rideshare.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_type', models.CharField(max_length=200)),
                ('max_passengers', models.IntegerField()),
                ('plate_number', models.CharField(max_length=200)),
                ('special_info', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ride_id', models.BigIntegerField()),
                ('status', models.CharField(max_length=200)),
                ('start_loc', models.CharField(max_length=200)),
                ('end_loc', models.CharField(max_length=200)),
                ('create_time', models.DateTimeField(verbose_name='time created')),
                ('end_time', models.DateTimeField(verbose_name='time completed')),
                ('driver_user', models.ForeignKey(on_delete=models.SET(rideshare.models.get_default_driver), to='rideshare.driver')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name_text', models.CharField(max_length=200)),
                ('last_name_text', models.CharField(max_length=200)),
                ('password_text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='RideUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ride_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rideshare.ride')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rideshare.user')),
            ],
        ),
        migrations.CreateModel(
            name='Rider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rideshare.user')),
            ],
        ),
        migrations.AddField(
            model_name='ride',
            name='request_user',
            field=models.ForeignKey(on_delete=models.SET(rideshare.models.get_default_rider), to='rideshare.rider'),
        ),
        migrations.AddField(
            model_name='driver',
            name='user',
            field=models.ForeignKey(on_delete=models.SET(rideshare.models.get_default_user), to='rideshare.user'),
        ),
    ]
