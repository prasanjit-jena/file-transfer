# Generated by Django 4.2.14 on 2024-07-19 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessedData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('month', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=100)),
                ('clubbed_name', models.CharField(max_length=100)),
                ('product', models.CharField(max_length=100)),
                ('value', models.FloatField()),
            ],
        ),
        migrations.DeleteModel(
            name='UploadedFile',
        ),
    ]
