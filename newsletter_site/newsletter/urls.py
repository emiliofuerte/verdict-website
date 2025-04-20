# newsletter/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.current_issue, name='current_issue'),
    path('past/', views.past_issues, name='past_issues'),
    path('article/<int:article_id>/', views.show_article, name='show_article'),
    path('submissions/', views.submissions, name='submissions'),
    path('join/', views.join_our_team, name='join_our_team'),
    path('about/', views.about_us, name='about_us'),

    # Author pages
    path('authors/', views.authors_index, name='authors_index'),
    path('author/<slug:slug>/', views.author_detail, name='author_detail'),

    # Legacy volume/issue/title route
    path(
        '<int:volume_number>/<int:issue_number>/<slug:short_title>/',
        views.show_article_by_volume_issue_title,
        name='show_article_by_volume_issue_title'
    ),
]