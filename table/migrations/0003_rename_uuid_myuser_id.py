# Generated by Django 4.1 on 2023-03-08 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('table', '0002_remove_myuser_id_alter_myuser_uuid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myuser',
            old_name='uuid',
            new_name='id',
        ),
    ]