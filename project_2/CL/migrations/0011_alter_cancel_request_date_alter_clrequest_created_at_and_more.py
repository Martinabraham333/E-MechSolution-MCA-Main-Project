# Generated by Django 4.1.6 on 2023-05-01 15:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CL', '0010_alter_cancel_request_date_alter_clrequest_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cancel_request',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 5, 1, 15, 38, 53, 369536), null=True),
        ),
        migrations.AlterField(
            model_name='clrequest',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 5, 1, 15, 38, 53, 369536), null=True),
        ),
        migrations.AlterField(
            model_name='mul_clrequest',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 5, 1, 15, 38, 53, 369536), null=True),
        ),
    ]
