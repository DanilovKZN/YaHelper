# Generated by Django 2.2.16 on 2022-04-24 14:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0026_auto_20220130_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infouser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
