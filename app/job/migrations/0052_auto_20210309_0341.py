# Generated by Django 2.1.1 on 2021-03-09 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0051_auto_20210309_0339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='part_rank',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Part Rank'),
        ),
    ]