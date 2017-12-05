# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagepersona', '0003_auto_20171204_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='json_response',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='albums',
            field=models.ManyToManyField(blank=True, to='imagepersona.ImageFolder'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='coverpic',
            field=models.ImageField(default='coverpic.jpg', upload_to='users/', verbose_name='Cover Pic'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profilepic',
            field=models.ImageField(default='profilepic.jpg', upload_to='users/', verbose_name='Profile Pic'),
        ),
    ]
