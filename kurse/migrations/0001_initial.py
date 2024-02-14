# Generated by Django 5.0.1 on 2024-02-06 17:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('kunden', '0001_initial'),
        ('trainer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Kurs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('va_nummer', models.IntegerField(unique=True)),
                ('thema', models.CharField(default='Outlook', max_length=50)),
                ('kurs_start', models.DateTimeField(blank=True, null=True)),
                ('kurs_ende', models.DateTimeField(blank=True, null=True)),
                ('kunde', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='kurse', to='kunden.kunde')),
                ('trainer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='kurse', to='trainer.trainer')),
            ],
        ),
    ]
