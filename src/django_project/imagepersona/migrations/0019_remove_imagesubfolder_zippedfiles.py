# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagepersona', '0018_auto_20171209_1027'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagesubfolder',
            name='zippedFiles',
        ),
    ]
