# Generated by Django 2.2.16 on 2022-01-24 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0022_remove_comment_image'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='ban on signing'),
        ),
    ]
