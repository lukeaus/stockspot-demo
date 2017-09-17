# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-17 09:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('advisors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=255)),
                ('hin', models.CharField(max_length=255)),
                ('advisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advisors.Advisor')),
            ],
        ),
    ]
