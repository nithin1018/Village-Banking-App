# Generated by Django 5.2.3 on 2025-06-23 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user_accounts", "0011_profile_otp_profile_otp_created_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="otp",
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
