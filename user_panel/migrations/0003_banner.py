# Generated by Django 4.2.5 on 2023-10-18 05:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_panel", "0002_cart_coupon"),
    ]

    operations = [
        migrations.CreateModel(
            name="banner",
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
                ("image", models.ImageField(upload_to="banners/")),
                ("title", models.CharField(max_length=256)),
            ],
        ),
    ]