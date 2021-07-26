from django.urls import path
from .views import (
    home, tweet_detail_view, tweet_list_view,
    tweet_create_view, tweet_delete_view, tweet_action_view)

urlpatterns = [
    path('', home, name='home'),
    path('create-tweet', tweet_create_view),
    path('tweets', tweet_list_view, name='all-tweets'),
    path('tweets/<int:tweet_id>', tweet_detail_view),
    path('api/tweets/action', tweet_action_view),
    path('api/tweets/<int:tweet_id>/delete', tweet_delete_view),
]