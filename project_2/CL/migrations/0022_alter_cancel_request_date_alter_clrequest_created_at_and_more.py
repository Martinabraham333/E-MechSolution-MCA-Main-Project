# Generated by Django 4.1.6 on 2023-05-08 10:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CL', '0021_rename_cancel_cl_history_cancel_request_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cancel_request',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 5, 8, 10, 3, 40, 871962), null=True),
        ),
        migrations.AlterField(
            model_name='clrequest',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 5, 8, 10, 3, 40, 871962), null=True),
        ),
        migrations.AlterField(
            model_name='mul_clrequest',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 5, 8, 10, 3, 40, 871962), null=True),
        ),
    ]
