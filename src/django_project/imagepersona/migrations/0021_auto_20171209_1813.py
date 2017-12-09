# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagepersona', '0020_verifyemail_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='verifyemail',
            name='status',
        ),
        migrations.AddField(
            model_name='linksharing',
            name='status',
            field=models.CharField(default='false', max_length=10),
            preserve_default=False,
        ),
    ]
