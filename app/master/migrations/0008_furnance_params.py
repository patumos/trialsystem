# Generated by Django 2.1.1 on 2019-04-02 05:07

from django.db import migrations
import jsonfield.encoder
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0007_furnance_template_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='furnance',
            name='params',
            field=jsonfield.fields.JSONField(blank=True, dump_kwargs={'cls': jsonfield.encoder.JSONEncoder, 'separators': (',', ':')}, load_kwargs={}, null=True),
        ),
    ]
