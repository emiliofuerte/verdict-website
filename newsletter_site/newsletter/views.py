# newsletter/views.py

from django.shortcuts import render, get_object_or_404
from .models import Article, Author
from collections import defaultdict

def current_issue(request):
    articles = Article.objects.filter(is_current_issue=True).order_by(
        "-volume_number", "-issue_number", "title"
    )
    grouped = defaultdict(lambda: defaultdict(list))
    for a in articles:
        grouped[a.volume_number][a.issue_number].append(a)

    sorted_volumes = sorted(grouped.keys(), reverse=True)
    context = {
        "grouped_volumes": [
            (v, sorted(grouped[v].items(), key=lambda x: x[0], reverse=True))
            for v in sorted_volumes
        ]
    }
    return render(request, 'newsletter/current_issue.html', context)

def past_issues(request):
    articles = Article.objects.filter(is_current_issue=False).order_by(
        "-volume_number", "-issue_number", "title"
    )
    grouped = defaultdict(lambda: defaultdict(list))
    for a in articles:
        grouped[a.volume_number][a.issue_number].append(a)

    sorted_volumes = sorted(grouped.keys(), reverse=True)
    grouped_volumes = []
    for vol_num in sorted_volumes:
        issues_dict = grouped[vol_num]
        sorted_issues = sorted(issues_dict.items(), key=lambda x: x[0], reverse=True)
        grouped_volumes.append((vol_num, sorted_issues))

    return render(request, 'newsletter/past_issues.html', {
        "grouped_volumes": grouped_volumes
    })

def show_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'newsletter/show_article.html', {"article": article})

def show_article_by_volume_issue_title(request, volume_number, issue_number, short_title):
    article = get_object_or_404(
        Article,
        volume_number=volume_number,
        issue_number=issue_number,
        short_title=short_title
    )
    return render(request, 'newsletter/show_article.html', {"article": article})

def submissions(request):
    return render(request, 'newsletter/submissions.html')

def join_our_team(request):
    return render(request, 'newsletter/join_our_team.html')

def about_us(request):
    # Fetch all authors for the contributors section
    authors = Author.objects.order_by('name')
    return render(request, 'newsletter/about_us.html', {
        'authors': authors,
    })

def authors_index(request):
    """List all authors alphabetically."""
    authors = Author.objects.order_by('name')
    return render(request, 'newsletter/authors_index.html', {
        'authors': authors,
    })

def author_detail(request, slug):
    """Show an author's profile and their articles."""
    author = get_object_or_404(Author, slug=slug)
    articles = author.articles.order_by(
        '-date', '-volume_number', '-issue_number', 'title'
    )
    return render(request, 'newsletter/author_detail.html', {
        'author': author,
        'articles': articles,
    })