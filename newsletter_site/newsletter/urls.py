# newsletter/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Home / Current Issue
    path('', views.current_issue, name='current_issue'),
    
    # Past Issues
    path('past-issues/', views.past_issues, name='past_issues'),
    
    # Submissions, Join, About
    path('submissions/', views.submissions, name='submissions'),
    path('join-our-team/', views.join_our_team, name='join_our_team'),
    path('about-us/', views.about_us, name='about_us'),

    # (Optional) Old path by article ID if you want to keep it
    path('article/<int:article_id>/', views.show_article, name='show_article'),

    # New path by volume/issue/short_title (make sure the name matches get_absolute_url)
    path(
        '<int:volume_number>/<int:issue_number>/<slug:short_title>/',
        views.show_article_by_volume_issue_title,
        name='show_article_by_volume_issue_title'
    ),
]