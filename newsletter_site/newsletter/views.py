from django.shortcuts import render

def current_issue(request):
    return render(request, 'newsletter/current_issue.html')

def past_issues(request):
    return render(request, 'newsletter/past_issues.html')

def submissions(request):
    return render(request, 'newsletter/submissions.html')

def join_our_team(request):
    return render(request, 'newsletter/join_our_team.html')

def about_us(request):
    return render(request, 'newsletter/about_us.html')
