# Generated by Django 4.2.5 on 2023-10-13 12:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_cart", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coupon",
            name="expiration_date",
            field=models.DateField(auto_now_add=True),
        ),
    ]
