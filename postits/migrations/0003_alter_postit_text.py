# Generated by Django 4.2.4 on 2023-08-29 13:00

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('postits', '0002_alter_postit_position_x_alter_postit_position_y'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postit',
            name='text',
            field=ckeditor.fields.RichTextField(),
        ),
    ]