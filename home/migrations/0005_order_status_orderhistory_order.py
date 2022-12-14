# Generated by Django 4.1.2 on 2022-11-14 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(default='Confirmed', max_length=100),
        ),
        migrations.AddField(
            model_name='orderhistory',
            name='order',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='home.order'),
        ),
    ]
