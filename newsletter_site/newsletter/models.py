from django.db import models

class Article(models.Model):
    """
    A model representing a single article in your newsletter.
    """
    doc_id = models.CharField(
        max_length=255, 
        help_text="The Google Drive file ID for this article's Doc."
    )
    title = models.CharField(max_length=255, blank=True, help_text="Optional local title.")
    content_html = models.TextField(
        blank=True, 
        help_text="Stores the HTML content fetched from Google Docs."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or f"Article (Doc ID {self.doc_id})"