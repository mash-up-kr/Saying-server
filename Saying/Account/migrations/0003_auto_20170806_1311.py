# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-08-06 13:11
from __future__ import unicode_literals

import Account.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0002_auto_20170804_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_profile_img',
            field=models.ImageField(default='profile/default.png', upload_to=Account.models.update_filename, verbose_name='프로필 사진'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='userid',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
