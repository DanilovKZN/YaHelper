# Generated by Django 2.2.9 on 2022-01-09 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_auto_20220109_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='posts/', verbose_name='Изображение'),
        ),
    ]
