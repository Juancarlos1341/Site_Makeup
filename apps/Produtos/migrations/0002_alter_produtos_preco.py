# Generated by Django 4.0.2 on 2022-04-21 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Produtos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produtos',
            name='preco',
            field=models.DecimalField(decimal_places=2, max_digits=100),
        ),
    ]
