# Generated by Django 4.2.2 on 2023-08-03 05:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planet', '0006_alter_planetdata_selected_poster'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planetdata',
            name='moon_panel',
        ),
        migrations.RemoveField(
            model_name='planetdata',
            name='screenshort',
        ),
    ]
