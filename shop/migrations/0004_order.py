# Generated by Django 2.2.7 on 2020-01-03 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('item_json', models.CharField(max_length=5000)),
                ('name', models.CharField(max_length=80)),
                ('email', models.CharField(max_length=80)),
                ('address', models.CharField(max_length=150)),
                ('city', models.CharField(max_length=80)),
                ('state', models.CharField(max_length=80)),
                ('zip_code', models.CharField(max_length=20)),
            ],
        ),
    ]
