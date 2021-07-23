from django.urls import path
from .views import home, tweet_detail_view, tweet_list_view, tweet_create_view

urlpatterns = [
    path('', home, name='home'),
    path('create-tweet', tweet_create_view),
    path('tweets', tweet_list_view, name='all-tweets'),
    path('tweets/<int:tweet_id>', tweet_detail_view),
]