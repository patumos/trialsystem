# Generated by Django 2.1.1 on 2019-04-03 02:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0011_furnance_tparams'),
        ('job', '0010_jobfurnance_keys'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='main_furnance',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='master.Furnance'),
        ),
    ]
