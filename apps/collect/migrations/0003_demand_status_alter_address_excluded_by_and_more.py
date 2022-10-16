# Generated by Django 4.0 on 2022-10-16 21:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_collector_excluded_by_and_more'),
        ('collect', '0002_auto_20220928_2100'),
    ]

    operations = [
        migrations.AddField(
            model_name='demand',
            name='status',
            field=models.CharField(choices=[('o', 'Open'), ('c', 'Closed'), ('p', 'Paused')], default='o', max_length=1),
        ),
        migrations.AlterField(
            model_name='address',
            name='excluded_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_excluded_by', to='core.user'),
        ),
        migrations.AlterField(
            model_name='addressdemand',
            name='excluded_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_excluded_by', to='core.user'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='excluded_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_excluded_by', to='core.user'),
        ),
    ]