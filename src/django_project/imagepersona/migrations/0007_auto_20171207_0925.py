# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagepersona', '0006_tags'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tags',
            new_name='ImageTag',
        ),
    ]
