# Generated by Django 5.1.6 on 2025-03-10 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register_user', '0006_alter_customuser_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlacklistedAccessToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jti', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
