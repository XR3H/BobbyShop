# Generated by Django 4.2.9 on 2024-02-12 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0002_attribute_itemattribute'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='itemattribute',
            unique_together={('fk_item', 'fk_attribute')},
        ),
    ]
