# Generated by Django 4.2.5 on 2023-10-16 06:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authenticator", "0003_alter_user_profile_wallet"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user_profile",
            name="wallet",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=13),
        ),
    ]