# Generated by Django 4.1.10 on 2023-07-24 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0005_alter_servedorder_counter_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='loadinglog',
            name='counter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='sales.counter'),
        ),
    ]
