# Generated by Django 4.1.3 on 2022-11-18 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_alter_event_options_alter_user_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='avatar.png', upload_to=''),
        ),
    ]