# Generated by Django 5.0.7 on 2024-08-04 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0002_weatherdata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weatherdata',
            name='last_updated',
        ),
        migrations.AddField(
            model_name='district',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
