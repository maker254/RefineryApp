# Generated by Django 4.1.10 on 2023-07-17 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0004_servedorder_delete_order_alter_counter_device_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servedorder',
            name='counter_no',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sales.counter'),
        ),
    ]
