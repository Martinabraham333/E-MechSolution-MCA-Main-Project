# Generated by Django 4.1.6 on 2023-05-09 21:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EM', '0034_alter_cancelreply_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cancelreply',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 5, 9, 21, 9, 28, 916616), null=True),
        ),
        migrations.AlterField(
            model_name='technicianreply',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 5, 9, 21, 9, 28, 916616), null=True),
        ),
    ]