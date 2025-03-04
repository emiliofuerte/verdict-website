# Generated by Django 4.2.5 on 2025-02-09 16:17

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Article",
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
                (
                    "doc_url",
                    models.TextField(
                        blank=True,
                        help_text="Paste the full Google Doc URL here. For example: https://docs.google.com/document/d/123abc456/edit",
                    ),
                ),
                (
                    "doc_id",
                    models.CharField(
                        blank=True,
                        help_text="Extracted automatically from the doc_url.",
                        max_length=255,
                    ),
                ),
                (
                    "content_html",
                    models.TextField(
                        blank=True,
                        help_text="HTML content fetched from the Google Doc.",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
