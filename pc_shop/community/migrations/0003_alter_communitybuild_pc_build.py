# Generated by Django 4.2.20 on 2025-03-17 02:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configurator', '0001_initial'),
        ('community', '0002_alter_communitybuild_pc_build'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communitybuild',
            name='pc_build',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='configurator.pcbuild'),
        ),
    ]
