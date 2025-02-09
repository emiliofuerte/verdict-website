# newsletter/urls.py
from django.urls import path
from . import views  # Import your view functions from views.py

urlpatterns = [
    path('', views.current_issue, name='current_issue'),
    path('past-issues/', views.past_issues, name='past_issues'),
    path('submissions/', views.submissions, name='submissions'),
    path('join-our-team/', views.join_our_team, name='join_our_team'),
    path('about-us/', views.about_us, name='about_us'),
]