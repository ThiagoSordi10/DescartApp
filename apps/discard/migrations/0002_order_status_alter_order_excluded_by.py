# Generated by Django 4.0 on 2022-10-16 21:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_collector_excluded_by_and_more'),
        ('discard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('a', 'Accepted'), ('r', 'Refused'), ('p', 'Pending')], default='p', max_length=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='excluded_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_excluded_by', to='core.user'),
        ),
    ]