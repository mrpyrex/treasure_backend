# Generated by Django 2.2 on 2020-03-19 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HouseCare',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('address', models.TextField()),
                ('host', models.CharField(max_length=250)),
                ('phone', models.CharField(max_length=13)),
            ],
            options={
                'verbose_name': 'house care fellowship center',
                'verbose_name_plural': 'House Care Fellowship Centers',
            },
        ),
    ]