# Generated by Django 4.2.4 on 2023-09-12 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Adresse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strasse', models.CharField(max_length=255)),
                ('plz', models.CharField(max_length=10)),
                ('stadt', models.CharField(max_length=255)),
                ('land', models.CharField(max_length=255)),
            ],
        ),
    ]