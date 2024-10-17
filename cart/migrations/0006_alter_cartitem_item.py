# Generated by Django 3.2.9 on 2024-10-16 21:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_category_description'),
        ('cart', '0005_alter_cartitem_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='catalog.item'),
        ),
    ]
