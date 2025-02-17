# Generated by Django 4.1.10 on 2023-07-14 05:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dbmaster', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EAS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=12)),
                ('moisture', models.DecimalField(decimal_places=2, max_digits=6)),
                ('chloride', models.DecimalField(decimal_places=2, max_digits=6)),
                ('calcium', models.DecimalField(decimal_places=2, max_digits=6)),
                ('magnesium', models.DecimalField(decimal_places=2, max_digits=6)),
                ('sulphates', models.DecimalField(decimal_places=2, max_digits=6)),
                ('alkalinity', models.DecimalField(decimal_places=2, max_digits=6)),
                ('insoluble_matter', models.DecimalField(decimal_places=2, max_digits=6)),
                ('iodine_min', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
                ('iodine_max', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
                ('sieve_size', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalCOA',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('sampling_date', models.DateField()),
                ('analysis_date', models.DateField()),
                ('batch_no', models.CharField(max_length=10)),
                ('moisture', models.DecimalField(decimal_places=2, max_digits=6)),
                ('chloride', models.DecimalField(decimal_places=2, max_digits=6)),
                ('calcium', models.DecimalField(decimal_places=2, max_digits=6)),
                ('magnesium', models.DecimalField(decimal_places=2, max_digits=6)),
                ('sulphates', models.DecimalField(decimal_places=2, max_digits=6)),
                ('alkalinity', models.DecimalField(decimal_places=2, max_digits=6)),
                ('insoluble_matter', models.DecimalField(decimal_places=2, max_digits=6)),
                ('iodine', models.DecimalField(decimal_places=2, max_digits=6)),
                ('sieve_size', models.CharField(max_length=6)),
                ('created', models.DateTimeField(blank=True, editable=False)),
                ('modified_by', models.CharField(blank=True, max_length=30, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('brand', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='dbmaster.brand')),
                ('eas', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='lab.eas')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('sample', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='lab.sample')),
            ],
            options={
                'verbose_name': 'historical coa',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='COA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sampling_date', models.DateField()),
                ('analysis_date', models.DateField()),
                ('batch_no', models.CharField(max_length=10)),
                ('moisture', models.DecimalField(decimal_places=2, max_digits=6)),
                ('chloride', models.DecimalField(decimal_places=2, max_digits=6)),
                ('calcium', models.DecimalField(decimal_places=2, max_digits=6)),
                ('magnesium', models.DecimalField(decimal_places=2, max_digits=6)),
                ('sulphates', models.DecimalField(decimal_places=2, max_digits=6)),
                ('alkalinity', models.DecimalField(decimal_places=2, max_digits=6)),
                ('insoluble_matter', models.DecimalField(decimal_places=2, max_digits=6)),
                ('iodine', models.DecimalField(decimal_places=2, max_digits=6)),
                ('sieve_size', models.CharField(max_length=6)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified_by', models.CharField(blank=True, max_length=30, null=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dbmaster.brand')),
                ('eas', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='lab.eas')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lab.sample')),
            ],
        ),
        migrations.AddConstraint(
            model_name='coa',
            constraint=models.UniqueConstraint(fields=('batch_no', 'brand', 'sampling_date'), name='unique_brand_batch'),
        ),
    ]
