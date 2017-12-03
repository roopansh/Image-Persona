# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('image', models.ImageField(max_length=50, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='ImageFolder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ImageSubFolder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('directory', models.ForeignKey(to='imagepersona.ImageFolder')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='imagefolder',
            name='owner',
            field=models.ForeignKey(to='imagepersona.UserProfile'),
        ),
        migrations.AddField(
            model_name='image',
            name='album',
            field=models.ForeignKey(to='imagepersona.ImageFolder'),
        ),
        migrations.AddField(
            model_name='image',
            name='people',
            field=models.ManyToManyField(to='imagepersona.ImageSubFolder'),
        ),
    ]
