# newsletter/models.py
from django.db import models
from django.utils.text import slugify
import re

DOC_URL_REGEX = re.compile(r'/document/d/([^/]+)/')

class Article(models.Model):
    # Basic metadata
    title = models.CharField(max_length=255, blank=True)
    writer = models.CharField(max_length=255, blank=True)
    date = models.DateField(null=True, blank=True)

    # Volume/Issue structure
    volume_number = models.PositiveIntegerField(default=1, help_text="Volume number")
    issue_number = models.PositiveIntegerField(default=1, help_text="Issue number")

    # Short version of the title for URL slugs
    short_title = models.SlugField(
        max_length=100,
        blank=True,
        help_text="Short URL-friendly version of the title"
    )

    # Preview text for homepage / listings
    preview_text = models.TextField(
        blank=True,
        help_text="Short preview or intro for the article"
    )

    # Article type choices
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

    # Google Doc fields
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
        # If we have a doc_url but no doc_id, extract it:
        if self.doc_url and not self.doc_id:
            match = DOC_URL_REGEX.search(self.doc_url)
            if match:
                self.doc_id = match.group(1)

        # Ensure short_title is never empty
        if not self.short_title:
            if self.title and self.title.strip():
                self.short_title = slugify(self.title)[:100]
            else:
                self.short_title = "untitled"

        super().save(*args, **kwargs)

    def __str__(self):
        # Display volume/issue info and title
        return f"{self.title or 'Untitled'} (Vol {self.volume_number}, Issue {self.issue_number})"

    def get_absolute_url(self):
        from django.urls import reverse
        # Uses the new route by volume, issue, and short_title
        return reverse(
            'show_article_by_volume_issue_title',
            args=[self.volume_number, self.issue_number, self.short_title]
        )