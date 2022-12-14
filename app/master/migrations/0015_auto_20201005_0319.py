# Generated by Django 2.1.1 on 2020-10-05 03:19

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0014_paramtemplate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='furnance',
            name='params',
            field=jsonfield.fields.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='furnance',
            name='tparams',
            field=jsonfield.fields.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='paramtemplate',
            name='qparams',
            field=jsonfield.fields.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='paramtemplate',
            name='tparams',
            field=jsonfield.fields.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='partmf',
            name='chtester1',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='partmf',
            name='chtester2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='partmf',
            name='designno',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='partmf',
            name='doc_code',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='partmf',
            name='effpoint1',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='partmf',
            name='effpoint2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='partmf',
            name='mat',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='partmf',
            name='othertester',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='partmf',
            name='partcode',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='partmf',
            name='partname',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='partmf',
            name='qo_no',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='partmf',
            name='shtester1',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='partmf',
            name='shtester2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='partmf',
            name='shtester3',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='partmf',
            name='size',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='partmf',
            name='treatcd',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
