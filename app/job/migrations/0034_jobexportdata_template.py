# Generated by Django 2.1.1 on 2019-04-30 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0033_auto_20190429_0740'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobexportdata',
            name='template',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
