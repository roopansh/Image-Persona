# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagepersona', '0014_auto_20171208_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagesubfolder',
            name='zippedFiles',
            field=models.FileField(null=True, upload_to=b'images/', blank=True),
        ),
    ]
