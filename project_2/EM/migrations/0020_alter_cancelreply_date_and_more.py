# Generated by Django 4.1.6 on 2023-05-05 23:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EM', '0019_alter_cancelreply_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cancelreply',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 5, 5, 23, 10, 8, 588248), null=True),
        ),
        migrations.AlterField(
            model_name='technicianreply',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 5, 5, 23, 10, 8, 588248), null=True),
        ),
    ]