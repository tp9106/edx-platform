# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import xmodule_django.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Average',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=4, db_index=True)),
                ('average01', models.CharField(max_length=255)),
                ('average02', models.CharField(max_length=255)),
                ('average03', models.CharField(max_length=255)),
                ('average04', models.CharField(max_length=255)),
                ('average05', models.CharField(max_length=255)),
                ('average06', models.CharField(max_length=255)),
                ('average07', models.CharField(max_length=255)),
                ('average08', models.CharField(max_length=255)),
                ('average09', models.CharField(max_length=255)),
                ('average10', models.CharField(max_length=255)),
                ('average11', models.CharField(max_length=255)),
                ('average12', models.CharField(max_length=255)),
                ('average13', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='DiagnosisInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course_id', xmodule_django.models.CourseKeyField(max_length=255, db_index=True)),
                ('finished', models.BooleanField(default=False)),
                ('finished_date', models.DateTimeField(null=True)),
                ('regulation_state', models.IntegerField(null=True)),
                ('timestamp1', models.DateTimeField(null=True, blank=True)),
                ('timestamp2_1', models.DateTimeField(null=True, blank=True)),
                ('timestamp2_2', models.DateTimeField(null=True, blank=True)),
                ('timestamp3', models.DateTimeField(null=True, blank=True)),
                ('timestamp4', models.DateTimeField(null=True, blank=True)),
                ('block1_01_1', models.CharField(max_length=255, blank=True)),
                ('block1_01_2', models.CharField(max_length=255, blank=True)),
                ('block1_02_1', models.CharField(max_length=255, blank=True)),
                ('block1_02_2', models.CharField(max_length=255, blank=True)),
                ('block1_03', models.CharField(max_length=2, blank=True)),
                ('block1_04_1', models.CharField(max_length=4, blank=True)),
                ('block1_04_2', models.CharField(max_length=2, blank=True)),
                ('block1_04_3', models.CharField(max_length=2, blank=True)),
                ('block1_05', models.EmailField(max_length=75, blank=True)),
                ('block2_01', models.CharField(max_length=16, blank=True)),
                ('block2_02', models.CharField(max_length=1, blank=True)),
                ('block2_03', models.CharField(max_length=1, blank=True)),
                ('block2_04', models.CharField(max_length=1, blank=True)),
                ('block2_05', models.CharField(max_length=1, blank=True)),
                ('block2_06', models.CharField(max_length=1, blank=True)),
                ('block2_07', models.CharField(max_length=1, blank=True)),
                ('block2_08', models.CharField(max_length=1, blank=True)),
                ('block2_09', models.CharField(max_length=1, blank=True)),
                ('block2_10', models.CharField(max_length=1, blank=True)),
                ('block2_11', models.CharField(max_length=1, blank=True)),
                ('block2_12', models.CharField(max_length=1, blank=True)),
                ('block2_13', models.CharField(max_length=1, blank=True)),
                ('block2_14', models.CharField(max_length=1, blank=True)),
                ('block2_15', models.CharField(max_length=1, blank=True)),
                ('block2_16', models.CharField(max_length=1, blank=True)),
                ('block2_17', models.CharField(max_length=1, blank=True)),
                ('block2_18', models.CharField(max_length=1, blank=True)),
                ('block2_19', models.CharField(max_length=1, blank=True)),
                ('block2_20', models.CharField(max_length=1, blank=True)),
                ('block2_21', models.CharField(max_length=1, blank=True)),
                ('block2_22', models.CharField(max_length=1, blank=True)),
                ('block2_23', models.CharField(max_length=1, blank=True)),
                ('block2_24', models.CharField(max_length=1, blank=True)),
                ('block2_25', models.CharField(max_length=1, blank=True)),
                ('block2_26', models.CharField(max_length=1, blank=True)),
                ('block2_27', models.CharField(max_length=1, blank=True)),
                ('block2b_3', models.CharField(max_length=3, blank=True)),
                ('block3_01', models.CharField(max_length=255, blank=True)),
                ('block3_02', models.CharField(max_length=255, blank=True)),
                ('block3_03_1', models.CharField(max_length=5, blank=True)),
                ('block3_03_2', models.CharField(max_length=5, blank=True)),
                ('block3_03_3', models.CharField(max_length=5, blank=True)),
                ('block3_04', models.CharField(max_length=255, blank=True)),
                ('block3_05', models.CharField(max_length=255, blank=True)),
                ('block3_06', models.CharField(max_length=255, blank=True)),
                ('block3_07', models.CharField(max_length=3, blank=True)),
                ('block3_08', models.CharField(max_length=255, blank=True)),
                ('block3_09_1', models.CharField(max_length=4, blank=True)),
                ('block3_09_2', models.CharField(max_length=2, blank=True)),
                ('block3_09_3', models.CharField(max_length=4, blank=True)),
                ('block3_09_4', models.CharField(max_length=2, blank=True)),
                ('block3_10', models.CharField(max_length=20, blank=True)),
                ('block3_11', models.CharField(max_length=20, blank=True)),
                ('block3_12', models.CharField(max_length=4, blank=True)),
                ('block3_13', models.CharField(max_length=4, blank=True)),
                ('block3_14', models.CharField(max_length=20, blank=True)),
                ('block3_15', models.CharField(max_length=255, blank=True)),
                ('block3_16', models.CharField(max_length=1024, blank=True)),
                ('block3_17', models.CharField(max_length=255, blank=True)),
                ('block3_18', models.CharField(max_length=4, blank=True)),
                ('block3_19', models.CharField(max_length=4, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GeneratePDFState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('download_url', models.CharField(default=b'', max_length=255, blank=True)),
                ('status', models.CharField(default=b'generating', max_length=32)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('error_reason', models.CharField(default=b'', max_length=512, blank=True)),
                ('key', models.CharField(default=b'', max_length=32, blank=True)),
                ('diagnosis_info', models.OneToOneField(to='ga_diagnosis.DiagnosisInfo')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='diagnosisinfo',
            unique_together=set([('user', 'course_id')]),
        ),
    ]
