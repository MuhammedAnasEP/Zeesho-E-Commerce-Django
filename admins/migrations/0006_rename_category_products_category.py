# Generated by Django 4.1.2 on 2022-10-28 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0005_alter_products_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='category',
            new_name='Category',
        ),
    ]
