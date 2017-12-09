# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagepersona', '0016_remove_imagesubfolder_zippedfiles'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagesubfolder',
            name='zippedFiles',
            field=models.FileField(null=True, upload_to=b'images/', blank=True),
        ),
    ]
