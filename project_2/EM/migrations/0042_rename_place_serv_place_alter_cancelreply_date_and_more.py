# Generated by Django 4.1.6 on 2023-05-31 10:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EM', '0041_place_alter_cancelreply_date_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='place',
            new_name='serv_place',
        ),
        migrations.AlterField(
            model_name='cancelreply',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 5, 31, 10, 18, 33, 616039), null=True),
        ),
        migrations.AlterField(
            model_name='technicianreply',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 5, 31, 10, 18, 33, 616039), null=True),
        ),
    ]
