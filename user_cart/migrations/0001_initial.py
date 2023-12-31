# Generated by Django 4.2.5 on 2023-10-13 11:19

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="coupon",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=128, unique=True)),
                ("discount", models.DecimalField(decimal_places=2, max_digits=5)),
                ("expiration_date", models.DateField(auto_now=True)),
                ("minimum_amount", models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]
