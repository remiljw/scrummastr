# Generated by Django 2.1.5 on 2019-03-29 00:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('remiljscrumy', '0004_auto_20190327_0259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scrumygoals',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='remiljscrumy.ScrumUser'),
        ),
    ]
