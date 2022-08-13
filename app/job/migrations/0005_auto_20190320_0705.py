# Generated by Django 2.1.1 on 2019-03-20 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0005_auto_20190319_1643'),
        ('job', '0004_jobfurnance'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobfurnance',
            name='furnance',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='master.Furnance'),
        ),
        migrations.AddField(
            model_name='jobfurnance',
            name='job',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='job.Job'),
        ),
    ]
