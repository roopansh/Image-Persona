# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagepersona', '0015_imagesubfolder_zippedfiles'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagesubfolder',
            name='zippedFiles',
        ),
    ]
