from django.conf import settings
from django.db import models
from random import randint

User = settings.AUTH_USER_MODEL


class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey('Tweets', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Tweets(models.Model):
    # on_delete models.SET_NULL, null=True to keep the tweets even when the user is gone
    user = models.ForeignKey(User, on_delete=models.CASCADE) # many users can own many tweets, but one tweet belongs to one user
    content = models.TextField(blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='tweet_user', blank=True, through=TweetLike)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": randint(0, 120)
        }