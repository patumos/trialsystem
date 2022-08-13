# Generated by Django 2.1.1 on 2019-03-20 03:22

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0002_job_safety'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='boutan',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='job',
            name='chagerate_kg',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='charttime',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='dumming_shutter_high',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='hand_setting',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='job',
            name='hopper_auto',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='job',
            name='prev_wash_notneed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='job',
            name='prev_wash_tbo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='job',
            name='prev_wash_tbt',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='job',
            name='prev_wash_tow',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='job',
            name='prev_wash_trw',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='job',
            name='rust_prevention',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='job',
            name='rust_prevention_comment',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='totalweight',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='vibration_level',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='safety',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('safe1', 'Safe1'), ('safe2', 'Safe2')], max_length=11, null=True, verbose_name='Safety Protective'),
        ),
    ]