# Generated by Django 4.1.6 on 2023-05-01 08:49

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CL', '0003_rating_technician_mul_clrequest_cl_mul_clrequest_em_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cancel_request',
            name='cl_mul_request',
        ),
        migrations.RemoveField(
            model_name='cancel_request',
            name='cl_request',
        ),
        migrations.AddField(
            model_name='cancel_request',
            name='service_mul_request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CL.mul_clrequest'),
        ),
        migrations.AddField(
            model_name='cancel_request',
            name='service_request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CL.clrequest'),
        ),
        migrations.AddField(
            model_name='clrequest',
            name='request_status',
            field=models.CharField(blank=True, default='pending', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='cancel_request',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 5, 1, 8, 49, 42, 166090), null=True),
        ),
        migrations.AlterField(
            model_name='clrequest',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 5, 1, 8, 49, 42, 166090), null=True),
        ),
        migrations.AlterField(
            model_name='mul_clrequest',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 5, 1, 8, 49, 42, 166090), null=True),
        ),
    ]