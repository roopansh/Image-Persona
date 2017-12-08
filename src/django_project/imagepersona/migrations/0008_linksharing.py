# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagepersona', '0007_auto_20171207_0925'),
    ]

    operations = [
        migrations.CreateModel(
            name='linksharing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reference', models.CharField(max_length=50)),
                ('real', models.CharField(max_length=80)),
            ],
        ),
    ]
