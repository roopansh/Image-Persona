# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagepersona', '0013_imagesubfolder_croppeddp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagesubfolder',
            name='personid',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
