# Generated by Django 2.1.1 on 2019-06-12 04:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0011_furnance_tparams'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(blank=True, max_length=200, null=True)),
                ('file', models.FileField(upload_to='images/%Y/%m/%d/')),
                ('part', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='master.PartMF')),
            ],
        ),
    ]
