# Generated by Django 2.2.14 on 2020-08-16 23:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('legislators', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinancialDisclosure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=4)),
                ('elected_officer', models.CharField(blank=True, max_length=100)),
                ('candidate', models.CharField(blank=True, max_length=100)),
                ('legislator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='financial_disclosures', to='legislators.Legislator')),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('held_by', models.CharField(choices=[('Filer', 'Filer'), ('Spouse', 'Spouse'), ('Dependent', 'Dependent')], max_length=50)),
                ('num_shares', models.CharField(max_length=100)),
                ('financial_disclosure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='finances.FinancialDisclosure')),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employer', models.CharField(max_length=100)),
                ('held_by', models.CharField(choices=[('Filer', 'Filer'), ('Spouse', 'Spouse'), ('Dependent', 'Dependent')], max_length=50)),
                ('position', models.CharField(blank=True, max_length=100)),
                ('financial_disclosure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='finances.FinancialDisclosure')),
            ],
        ),
        migrations.CreateModel(
            name='Gift',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('donor', models.CharField(max_length=100)),
                ('recipient', models.CharField(choices=[('Filer', 'Filer'), ('Spouse', 'Spouse'), ('Dependent', 'Dependent')], max_length=50)),
                ('description', models.CharField(max_length=100)),
                ('financial_disclosure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gifts', to='finances.FinancialDisclosure')),
            ],
        ),
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('held_by', models.CharField(choices=[('Filer', 'Filer'), ('Spouse', 'Spouse'), ('Dependent', 'Dependent')], max_length=50)),
                ('position', models.CharField(blank=True, max_length=100)),
                ('financial_disclosure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boards', to='finances.FinancialDisclosure')),
            ],
        ),
    ]
