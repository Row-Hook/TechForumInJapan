# Generated by Django 4.2.6 on 2023-11-13 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pages',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='更新日時'),
        ),
    ]
