# Generated by Django 3.0.8 on 2020-09-14 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_phone_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_traider',
            field=models.IntegerField(blank=True, choices=[('1', 'Company'), ('2', 'Self employed')], default=0, null=True),
        ),
    ]
