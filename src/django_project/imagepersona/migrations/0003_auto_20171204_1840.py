# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagepersona', '0002_auto_20171204_0741'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='coverpic',
            field=models.ImageField(default='https://media.istockphoto.com/photos/family-fun-time-in-the-sun-picture-id496799381?k=6&m=496799381&s=612x612&w=0&h=CIpSwwa2ZhRTeT13kgSYjkAMP76T15UKn0OOb0o86HQ=', verbose_name='Cover Pic', upload_to=''),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='profilepic',
            field=models.ImageField(default='https://i.pinimg.com/736x/25/c7/74/25c774fa39c0d33ca7cd1c5df7d107e9--men-portrait-photo-portrait.jpg', verbose_name='Profile Pic', upload_to=''),
        ),
    ]
