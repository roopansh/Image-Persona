# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagepersona', '0017_imagesubfolder_zippedfiles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagesubfolder',
            name='zippedFiles',
            field=models.FileField(null=True, upload_to=b'zippedImages/', blank=True),
        ),
    ]
