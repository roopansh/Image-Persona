# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagepersona', '0011_auto_20171208_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagesubfolder',
            name='displaypic',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='imagesubfolder',
            name='personid',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]
