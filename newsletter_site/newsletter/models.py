# newsletter/models.py
from django.db import models
import re

DOC_URL_REGEX = re.compile(r'/document/d/([^/]+)/')

class Article(models.Model):
    # Basic metadata
    title = models.CharField(max_length=255, blank=True)
    writer = models.CharField(max_length=255, blank=True)
    date = models.DateField(null=True, blank=True)
    issue_number = models.PositiveIntegerField(default=1)

    ARTICLE_TYPES = [
        ('op-ed', 'Op-Ed'),
        ('news', 'News'),
        ('features', 'Features'),
        ('other', 'Other'),
    ]
    article_type = models.CharField(
        max_length=50,
        choices=ARTICLE_TYPES,
        default='news'
    )

    doc_url = models.TextField(
        blank=True,
        help_text="Paste the full Google Doc URL here."
    )
    doc_id = models.CharField(
        max_length=255,
        blank=True,
        help_text="Auto-extracted from doc_url"
    )
    content_html = models.TextField(
        blank=True,
        help_text="Fetched HTML content from Google Docs."
    )

    is_current_issue = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.doc_url and not self.doc_id:
            match = DOC_URL_REGEX.search(self.doc_url)
            if match:
                self.doc_id = match.group(1)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title or 'Untitled'} (Issue {self.issue_number})"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('show_article', args=[str(self.id)])