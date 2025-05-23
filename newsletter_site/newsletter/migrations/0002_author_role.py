# Generated by Django 4.2.5 on 2025-04-21 12:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("newsletter", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="author",
            name="role",
            field=models.CharField(
                choices=[
                    ("director", "Director"),
                    ("lead editor", "Lead Editor"),
                    ("lead publisher", "Lead Publisher"),
                    ("treasurer", "Treasurer"),
                    ("social chair", "Social Chair"),
                    ("writer", "Writer"),
                    ("contributor", "Contributor"),
                ],
                default="Contributor",
                max_length=50,
            ),
        ),
    ]
