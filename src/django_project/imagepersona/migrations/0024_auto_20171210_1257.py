# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagepersona', '0023_apicalls'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apicalls',
            name='time',
            field=models.DateTimeField(),
        ),
    ]
