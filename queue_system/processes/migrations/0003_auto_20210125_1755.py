# Generated by Django 3.1.5 on 2021-01-25 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processes', '0002_process_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='process_user',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='process_user',
            name='completed_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='process_user',
            name='joined_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
