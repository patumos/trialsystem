# Generated by Django 2.1.1 on 2019-03-19 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0004_auto_20190318_0541'),
    ]

    operations = [
        migrations.AddField(
            model_name='partmf',
            name='total_low',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='partmf',
            name='total_up',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='partmf',
            name='total_measures',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
