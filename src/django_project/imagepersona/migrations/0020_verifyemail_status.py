# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagepersona', '0019_remove_imagesubfolder_zippedfiles'),
    ]

    operations = [
        migrations.AddField(
            model_name='verifyemail',
            name='status',
            field=models.CharField(default='false', max_length=10),
            preserve_default=False,
        ),
    ]
