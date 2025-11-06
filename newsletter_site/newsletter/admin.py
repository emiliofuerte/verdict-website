# newsletter/admin.py

from django.contrib import admin, messages
from .models import Author, Article
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
    for article in queryset:
        if not article.doc_id:
            messages.error(request, f"Article {article} has no doc_id to fetch.")
            continue
        metadata, html_content = fetch_doc_and_parse_metadata(article.doc_id)
        if not html_content:
            messages.error(request, f"Could not fetch doc {article.doc_id}.")
            continue

        article.title = metadata.get('title') or article.title
        article.writer = metadata.get('writer') or article.writer

        date_val = metadata.get('date')
        if date_val and hasattr(date_val, "year"):
            article.date = date_val

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
        "volume_number",
        "issue_number",
        "article_type",
        "is_current_issue",
        "display_order",
        "updated_at",
    )
    list_editable = ("volume_number", "issue_number", "is_current_issue", "display_order")
    search_fields = ("title", "writer", "short_title")
    list_filter = ("article_type", "is_current_issue")

    fieldsets = (
        (None, {
            "fields": (
                "title_image",
                "title",
                "short_title",
                "writer",
                "authors",
                "preview_text",
                "preview_image",
                "date",
                "article_type",
                "volume_number",
                "issue_number",
                "is_current_issue",
                "display_order",
            )
        }),
        ("Google Doc Info", {
            "classes": ("collapse",),
            "fields": ("doc_url", "doc_id", "content_html"),
        }),
    )

    actions = [mark_as_current, mark_as_past, fetch_doc_and_metadata]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "role", "article_count")
    prepopulated_fields = {"slug": ("name",)}
    fields = ("name", "slug", "role", "bio", "headshot")

    def article_count(self, obj):
        return obj.articles.count()
    article_count.short_description = "Articles"