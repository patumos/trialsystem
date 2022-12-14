# Generated by Django 2.1.1 on 2019-04-08 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0022_job_updated_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobInspection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inspection_item', models.CharField(choices=[('surface-hardness', 'Surface Hardness'), ('core-hardness', 'Core Hardness'), ('internal-hardness', 'Internal Hardness'), ('eff-e550', 'Effective Case-Depth E(550)'), ('eff-e465', 'Effective Case-Depth E(465)'), ('eff-e450', 'Effective Case-Depth E(450)'), ('eff-e400', 'Effective Case-Depth E(400)'), ('eff-e350', 'Effective Case-Depth E(350)'), ('eff-e513', 'Effective Case-Depth E(513)'), ('eff-e363', 'Effective Case-Depth E(363)'), ('eff-e420', 'Effective Case-Depth E(420)'), ('eff-e300', 'Effective Case-Depth E(300)'), ('eff-e390', 'Effective Case-Depth E(390)'), ('eff-e580', 'Effective Case-Depth E(580)'), ('eff-e440', 'Effective Case-Depth E(440)'), ('eff-e600', 'Effective Case-Depth E(600)'), ('eff-e360', 'Effective Case-Depth E(360)'), ('eff-e500', 'Effective Case-Depth E(500)'), ('eff-e593', 'Effective Case-Depth E(593)'), ('eff-e700', 'Effective Case-Depth E(700)'), ('eff-e392', 'Effective Case-Depth E(392)'), ('eff-e446', 'Effective Case-Depth E(446)'), ('eff-e530', 'Effective Case-Depth E(530)'), ('total-case-depth', 'Total case depth'), ('micro', 'Micro-structure')], max_length=100)),
                ('tester', models.CharField(choices=[('MHv10g.', 'MHv10g.'), ('MHv25g.', 'MHv25g.'), ('MHv50g.', 'MHv50g.'), ('MHv100g.', 'MHv100g.'), ('MHv200g.', 'MHv200g.'), ('MHv300g.', 'MHv300g.'), ('MHv500g.', 'MHv300g.'), ('MHv1Kg.', 'MHv1Kg.'), ('Hv5Kg.', 'Hv5Kg.'), ('Hv10Kg.', 'Hv10Kg.'), ('Hv20Kg.', 'Hv20Kg.'), ('Hv30Kg.', 'Hv30Kg.'), ('Hv50Kg.', 'Hv50Kg.'), ('HR15N', 'HR15N'), ('HR30N', 'HR30N'), ('HRA', 'HRA'), ('HRB', 'HRB'), ('HRC', 'HRC'), ('HS', 'HS'), ('HB', 'HB'), ('Micro scope (x50)', 'Micro scope (x50)'), ('Micro scope (x100)', 'Micro scope (x100)'), ('Micro scope (x400)', 'Micro scope (x400)'), ('Micro scope (x100,x400)', 'Micro scope (x100,x400)'), ('Micro scope (x500)', 'Micro scope (x500)')], max_length=100)),
                ('sample_size', models.IntegerField()),
                ('sample_points', models.CharField(max_length=200)),
                ('sample_note', models.TextField(blank=True, null=True)),
                ('standard_note', models.TextField(blank=True, null=True)),
                ('job', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='job.Job')),
            ],
        ),
    ]
