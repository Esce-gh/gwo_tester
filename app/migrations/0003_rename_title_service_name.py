# Generated by Django 5.2 on 2025-04-22 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_page_page_num'),
    ]

    operations = [
        migrations.RenameField(
            model_name='service',
            old_name='title',
            new_name='name',
        ),
    ]
