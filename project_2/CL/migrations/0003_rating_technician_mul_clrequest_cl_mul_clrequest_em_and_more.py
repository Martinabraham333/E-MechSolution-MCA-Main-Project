# Generated by Django 4.1.6 on 2023-04-30 21:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CL', '0002_cancel_request_clients_clprofile_clrequest_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('EM', '0003_remove_emprofiles_mobile_remove_emprofiles_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='technician',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='EM.technicians'),
        ),
        migrations.AddField(
            model_name='mul_clrequest',
            name='cl',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CL.clients'),
        ),
        migrations.AddField(
            model_name='mul_clrequest',
            name='em',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='EM.technicians'),
        ),
        migrations.AddField(
            model_name='clrequest',
            name='cl',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CL.clients'),
        ),
        migrations.AddField(
            model_name='clrequest',
            name='em',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='EM.technicians'),
        ),
        migrations.AddField(
            model_name='clprofile',
            name='cl',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CL.clients'),
        ),
        migrations.AddField(
            model_name='clients',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cancel_request',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CL.clients'),
        ),
        migrations.AddField(
            model_name='cancel_request',
            name='technician',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='EM.technicians'),
        ),
    ]