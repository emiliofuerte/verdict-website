# newsletter/views.py
from django.shortcuts import render, get_object_or_404
from .models import Article
from collections import defaultdict

def current_issue(request):
    articles = Article.objects.filter(is_current_issue=True).order_by(
        "-volume_number", "-issue_number", "title"
    )
    # Nested grouping: volume -> issue -> list of articles
    grouped = defaultdict(lambda: defaultdict(list))
    for a in articles:
        grouped[a.volume_number][a.issue_number].append(a)

    # Sort volumes desc, then issues desc
    sorted_volumes = sorted(grouped.keys(), reverse=True)

    context = {
        "grouped_volumes": [
            (v, sorted(grouped[v].items(), key=lambda x: x[0], reverse=True))
            for v in sorted_volumes
        ]
    }
    return render(request, 'newsletter/current_issue.html', context)

def past_issues(request):
    # 1. Grab all articles with is_current_issue=False
    #    Sort by volume desc, then issue desc, then title
    articles = Article.objects.filter(is_current_issue=False).order_by(
        "-volume_number", "-issue_number", "title"
    )
    
    # 2. Group them by volume_number, then by issue_number
    grouped = defaultdict(lambda: defaultdict(list))
    for a in articles:
        grouped[a.volume_number][a.issue_number].append(a)

    # 3. Sort volumes in descending order
    sorted_volumes = sorted(grouped.keys(), reverse=True)

    # 4. Create a list of (volume_number, [(issue_number, [articles]), ...])
    grouped_volumes = []
    for vol_num in sorted_volumes:
        issues_dict = grouped[vol_num]
        # Sort the issues in descending order too
        sorted_issues = sorted(issues_dict.items(), key=lambda x: x[0], reverse=True)
        grouped_volumes.append((vol_num, sorted_issues))

    # 5. Send grouped_volumes to the template
    context = {
        "grouped_volumes": grouped_volumes
    }
    return render(request, 'newsletter/past_issues.html', context)

def show_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'newsletter/show_article.html', {"article": article})

def submissions(request):
    return render(request, 'newsletter/submissions.html')

def join_our_team(request):
    return render(request, 'newsletter/join_our_team.html')

def about_us(request):
    return render(request, 'newsletter/about_us.html')

def show_article_by_volume_issue_title(request, volume_number, issue_number, short_title):
    article = get_object_or_404(
        Article,
        volume_number=volume_number,
        issue_number=issue_number,
        short_title=short_title
    )
    return render(request, 'newsletter/show_article.html', {"article": article})