# Generated by Django 5.1.4 on 2025-01-21 09:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_wp_plugin_server', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plugin',
            name='active_version',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='active_for_plugins', to='app_wp_plugin_server.pluginversion'),
        ),
    ]
