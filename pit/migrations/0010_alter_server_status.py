# Generated by Django 4.2.4 on 2023-09-05 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pit', '0009_alter_server_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='status',
            field=models.CharField(choices=[('Lager', 'Lager'), ('Unterwegs', 'Unterwegs'), ('Zurücksetzen', 'Zurücksetzen'), ('Unbekannt', 'Unbekannt'), ('Rückholung', 'Rückholung'), ('Weiterleitung', 'Weiterleitung')], default='Zurücksetzen', max_length=255),
        ),
    ]
