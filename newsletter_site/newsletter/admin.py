# newsletter/admin.py
from django.contrib import admin, messages
from .models import Article
from .utils import fetch_doc_and_parse_metadata

@admin.action(description="Add to Current Issue")
def mark_as_current(modeladmin, request, queryset):
    updated = queryset.update(is_current_issue=True)
    messages.success(request, f"{updated} article(s) marked as current.")

@admin.action(description="Add to Past Issues")
def mark_as_past(modeladmin, request, queryset):
    updated = queryset.update(is_current_issue=False)
    messages.success(request, f"{updated} article(s) marked as past.")

@admin.action(description="Fetch Doc & Parse Metadata")
def fetch_doc_and_metadata(modeladmin, request, queryset):
    """
    Calls our fetch_doc_and_parse_metadata utility,
    sets fields on the Article, and saves.
    """
    for article in queryset:
        if not article.doc_id:
            messages.error(request, f"Article {article} has no doc_id to fetch.")
            continue

        metadata, html_content = fetch_doc_and_parse_metadata(article.doc_id)
        if not html_content:
            messages.error(request, f"Could not fetch doc {article.doc_id}.")
            continue

        # Update fields from metadata
        article.title = metadata.get('title') or article.title
        article.writer = metadata.get('writer') or article.writer

        # If the date is a datetime.date or a string, handle accordingly:
        date_val = metadata.get('date')
        if date_val:
            if hasattr(date_val, "year"):  # it's a date object
                article.date = date_val
            else:
                # It's a string fallback
                # If you prefer not to store raw strings, do something else
                pass

        if metadata.get('issue_number') is not None:
            article.issue_number = metadata['issue_number']

        if metadata.get('article_type'):
            article.article_type = metadata['article_type']

        article.content_html = html_content
        article.save()
        messages.success(request, f"Fetched & updated {article.title}.")

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "writer",
        "issue_number",
        "article_type",
        "is_current_issue",
        "updated_at",
    )
    list_editable = ("issue_number", "is_current_issue")
    search_fields = ("title", "writer")
    actions = [mark_as_current, mark_as_past, fetch_doc_and_metadata]