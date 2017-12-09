# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagepersona', '0012_auto_20171208_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagesubfolder',
            name='croppedDP',
            field=models.ImageField(null=True, upload_to=b'images/', blank=True),
        ),
    ]
