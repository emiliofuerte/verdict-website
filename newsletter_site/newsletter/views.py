# newsletter/views.py
from django.shortcuts import render, get_object_or_404
from .models import Article
from collections import defaultdict


def current_issue(request):
    # Instead of listing the entire content, group them by issue
    articles = Article.objects.filter(is_current_issue=True).order_by("-issue_number", "title")
    grouped = defaultdict(list)
    for a in articles:
        grouped[a.issue_number].append(a)
    # Sort by issue_number descending
    grouped_issues = sorted(grouped.items(), key=lambda x: x[0], reverse=True)

    return render(request, 'newsletter/current_issue.html', {
        "grouped_issues": grouped_issues
    })

def past_issues(request):
    articles = Article.objects.filter(is_current_issue=False).order_by("-issue_number", "title")
    grouped = defaultdict(list)
    for a in articles:
        grouped[a.issue_number].append(a)
    grouped_issues = sorted(grouped.items(), key=lambda x: x[0], reverse=True)

    return render(request, 'newsletter/past_issues.html', {
        "grouped_issues": grouped_issues
    })

def show_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'newsletter/show_article.html', {"article": article})

def submissions(request):
    return render(request, 'newsletter/submissions.html')

def join_our_team(request):
    return render(request, 'newsletter/join_our_team.html')

def about_us(request):
    return render(request, 'newsletter/about_us.html')