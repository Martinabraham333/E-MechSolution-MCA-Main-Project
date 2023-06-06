# Generated by Django 4.1.6 on 2023-05-09 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_tech_reg_email_tech_reg_first_name_tech_reg_password_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_reg',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='user_reg',
            name='first_name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='user_reg',
            name='password',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='user_reg',
            name='username',
            field=models.CharField(max_length=150, null=True),
        ),
    ]