# Generated by Django 4.2.9 on 2024-02-01 21:22

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import rideshare.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('rideshare', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OurUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='driver',
            name='special_info',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='driver',
            name='user',
            field=models.ForeignKey(on_delete=models.SET(rideshare.models.get_default_user), to='rideshare.ouruser'),
        ),
        migrations.AlterField(
            model_name='rider',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rideshare.ouruser'),
        ),
        migrations.AlterField(
            model_name='rideuser',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rideshare.ouruser'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]