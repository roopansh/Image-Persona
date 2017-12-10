# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagepersona', '0022_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='APIcalls',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.CharField(max_length=50)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
