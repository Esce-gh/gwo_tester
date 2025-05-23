# Generated by Django 5.2 on 2025-04-30 10:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_rating_comment_remove_rating_is_ok_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='criteria',
            field=models.CharField(choices=[('PN', 'Page Number Criteria'), ('HF', 'Header Footer Criteria'), ('OD', 'Object Detection Criteria')]),
        ),
        migrations.AlterField(
            model_name='service',
            name='criteria',
            field=models.CharField(choices=[('PN', 'Page Number Criteria'), ('HF', 'Header Footer Criteria'), ('OD', 'Object Detection Criteria')]),
        ),
        migrations.CreateModel(
            name='CriteriaHeaderFooter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header_visible', models.BooleanField()),
                ('header_detected', models.BooleanField()),
                ('footer_visible', models.BooleanField()),
                ('footer_detected', models.BooleanField()),
                ('rating', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to='app.rating')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CriteriaObjectDetection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visible_objects', models.IntegerField()),
                ('detected_objects', models.IntegerField()),
                ('rating', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to='app.rating')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
