# Generated by Django 5.1.6 on 2025-03-07 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
