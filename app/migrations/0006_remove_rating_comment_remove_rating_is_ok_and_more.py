# Generated by Django 5.2 on 2025-04-26 09:05

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_rating_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='is_ok',
        ),
        migrations.AddField(
            model_name='rating',
            name='criteria',
            field=models.CharField(choices=[('PN', 'Page Number Criteria')], default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='service',
            name='criteria',
            field=models.CharField(choices=[('PN', 'Page Number Criteria')], default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='CriteriaPageNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_number_visible', models.BooleanField()),
                ('page_number_detected', models.BooleanField()),
                ('rating', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to='app.rating')),
            ],
        ),
    ]
