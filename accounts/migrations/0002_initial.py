# Generated by Django 5.0.1 on 2024-02-18 16:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('crep', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='councilor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crep.councilor'),
        ),
        migrations.AddField(
            model_name='account',
            name='municipality',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crep.municipality'),
        ),
        migrations.AddField(
            model_name='account',
            name='province',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crep.province'),
        ),
        migrations.AddField(
            model_name='account',
            name='section_or_area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crep.rating'),
        ),
        migrations.AddField(
            model_name='account',
            name='ward',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crep.ward'),
        ),
        migrations.AddField(
            model_name='otp',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
