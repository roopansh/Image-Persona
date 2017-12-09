# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagepersona', '0010_image_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagesubfolder',
            name='displaypic',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='imagesubfolder',
            name='personid',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
    ]
