# Generated by Django 4.1.6 on 2023-05-01 12:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EM', '0008_alter_cancelreply_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cancelreply',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 5, 1, 12, 25, 28, 996826), null=True),
        ),
        migrations.AlterField(
            model_name='technicianreply',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 5, 1, 12, 25, 28, 996826), null=True),
        ),
    ]
