# Generated by Django 3.2.9 on 2021-11-27 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reserve', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='customer_number',
            field=models.IntegerField(default=0),
        ),
    ]
