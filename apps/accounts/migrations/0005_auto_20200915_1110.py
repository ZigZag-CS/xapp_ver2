# Generated by Django 3.0.8 on 2020-09-15 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200914_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_traider',
            field=models.IntegerField(blank=True, choices=[('0', 'User'), ('1', 'Company'), ('2', 'Self employed')], default=0, null=True),
        ),
    ]