# Generated by Django 4.2.2 on 2023-07-25 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vending', '0005_alter_vendingmachineslot_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendingmachineslot',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vending.product'),
        ),
    ]
