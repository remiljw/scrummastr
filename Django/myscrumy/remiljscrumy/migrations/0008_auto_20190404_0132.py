# Generated by Django 2.1.5 on 2019-04-04 00:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('remiljscrumy', '0007_auto_20190403_2347'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scrumygoals',
            options={'ordering': ['id'], 'verbose_name_plural': 'Scrumy Goals'},
        ),
        migrations.RemoveField(
            model_name='scrumygoals',
            name='goal_id',
        ),
    ]
