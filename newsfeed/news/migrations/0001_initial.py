# Generated by Django 2.2.5 on 2019-11-15 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewsInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_id', models.IntegerField()),
                ('pubDate', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255, unique=True)),
                ('link', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=1000)),
                ('imageLink', models.CharField(max_length=255)),
                ('imageDescription', models.CharField(max_length=255)),
            ],
        ),
    ]
