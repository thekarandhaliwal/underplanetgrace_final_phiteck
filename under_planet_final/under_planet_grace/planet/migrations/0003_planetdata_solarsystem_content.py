# Generated by Django 4.2.2 on 2023-07-31 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planet', '0002_planetdata_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='planetdata',
            name='solarsystem_content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
