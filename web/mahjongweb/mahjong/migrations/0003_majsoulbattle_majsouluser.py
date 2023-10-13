# Generated by Django 4.2.4 on 2023-09-23 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mahjong', '0002_yakuman'),
    ]

    operations = [
        migrations.CreateModel(
            name='Majsoulbattle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('User1', models.CharField(max_length=200)),
                ('User2', models.CharField(max_length=200)),
                ('User3', models.CharField(max_length=200)),
                ('point1', models.FloatField()),
                ('point2', models.FloatField()),
                ('point3', models.FloatField()),
                ('uuid', models.CharField(max_length=200)),
                ('date', models.DateTimeField(verbose_name='date battled')),
            ],
        ),
        migrations.CreateModel(
            name='Majsouluser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=200)),
                ('pt', models.FloatField()),
            ],
        ),
    ]