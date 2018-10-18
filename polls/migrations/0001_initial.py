# Generated by Django 2.1.2 on 2018-10-18 01:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DTSF01',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ROOM', models.CharField(max_length=3)),
                ('BEGIN_DATE', models.CharField(max_length=10)),
                ('NAME', models.CharField(max_length=20)),
                ('END_DATE', models.CharField(max_length=10)),
                ('CELL_PHONE', models.CharField(max_length=10)),
                ('RENT_AMT', models.IntegerField(default=0)),
                ('DIPOSIT', models.IntegerField(default=0)),
                ('PUB_DASHBOARD', models.CharField(max_length=3)),
                ('THIS_DEGREES', models.IntegerField(default=0)),
                ('TIMES', models.FloatField(default=0.0)),
                ('ADDRESS', models.CharField(max_length=50)),
                ('STATUS', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='DTSF02',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('INPUT_DATE', models.CharField(max_length=10)),
                ('LAST_DEGREES', models.IntegerField(default=0)),
                ('THIS_DEGREES', models.IntegerField(default=0)),
                ('RENT_AMT', models.IntegerField(default=0)),
                ('PUB_ELECTRIC_AMT', models.IntegerField(default=0)),
                ('ELECTRIC_AMT', models.IntegerField(default=0)),
                ('DIPOSIT_AMT', models.IntegerField(default=0)),
                ('TOTAL_AMT', models.IntegerField(default=0)),
                ('MESSAGE', models.CharField(max_length=200)),
                ('IS_CONF', models.BooleanField(default=False)),
                ('DTSF01', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.DTSF01')),
            ],
        ),
        migrations.CreateModel(
            name='DTSF03',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DASHBOARD', models.CharField(max_length=3)),
                ('THIS_DEGREES', models.IntegerField(default=0)),
                ('TIMES', models.FloatField(default=0.0)),
                ('AVG_NUM', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='DTSF04',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DASHBOARD', models.CharField(max_length=3)),
                ('INPUT_DATE', models.CharField(max_length=10)),
                ('LAST_DEGREES', models.IntegerField(default=0)),
                ('THIS_DEGREES', models.IntegerField(default=0)),
                ('ELECTRIC_AMT', models.IntegerField(default=0)),
                ('AVG_AMT', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room', models.CharField(max_length=4)),
                ('ChName', models.CharField(max_length=20)),
                ('begin_date', models.CharField(max_length=10)),
                ('end_date', models.CharField(max_length=10)),
                ('rent_amt', models.IntegerField(default=0)),
            ],
        ),
    ]
