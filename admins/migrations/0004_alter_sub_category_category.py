# Generated by Django 4.1.2 on 2022-10-26 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0003_sub_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sub_category',
            name='category',
            field=models.CharField(max_length=50),
        ),
    ]
