# Generated by Django 4.1.10 on 2023-07-17 07:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_counter_closed_alter_counter_is_running'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='counter',
            name='unique counter device',
        ),
    ]
