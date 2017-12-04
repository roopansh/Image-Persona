# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagepersona', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='album',
        ),
        migrations.RemoveField(
            model_name='image',
            name='people',
        ),
        migrations.RemoveField(
            model_name='imagefolder',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='imagesubfolder',
            name='directory',
        ),
        migrations.AddField(
            model_name='imagefolder',
            name='subfolders',
            field=models.ManyToManyField(to='imagepersona.ImageSubFolder'),
        ),
        migrations.AddField(
            model_name='imagesubfolder',
            name='images',
            field=models.ManyToManyField(to='imagepersona.Image'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='albums',
            field=models.ManyToManyField(to='imagepersona.ImageFolder'),
        ),
    ]
