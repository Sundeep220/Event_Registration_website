# Generated by Django 4.1.3 on 2022-11-20 13:49

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=django_resized.forms.ResizedImageField(crop=None, default='avatar.png', force_format='JPEG', keep_meta=True, quality=75, scale=0.5, size=[300, 300], upload_to=''),
        ),
    ]
