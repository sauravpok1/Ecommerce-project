# Generated by Django 2.2.7 on 2019-12-11 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_item_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='status',
            field=models.CharField(blank=True, choices=[('sale', 'sale'), ('hot', 'hot'), ('new', 'new'), ('', 'default')], max_length=100),
        ),
    ]
