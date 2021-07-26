from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

from .models import Tweets
from .serializers import TweetSerializer, TweetActionSerializer

ALLOWED_HOSTS = settings.ALLOWED_HOSTS
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS


def home(request, *args, **kwargs):
    return render(request, 'tweets/index.html', context={}, status=200)


@api_view(http_method_names=['POST'])
#  @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated]) # REST API course
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetSerializer(data=request.POST or None)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)


@api_view(http_method_names=['GET'])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweets.objects.all()
    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(http_method_names=['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    """
    REST API VIEW
    Consume by JS
    return JSON
    """
    qs = Tweets.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status=200)


@api_view(http_method_names=['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    """
    REST API VIEW
    Consume by JS
    return JSON
    """
    qs = Tweets.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({'message': 'You cannot delete this tweet'}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({'message': 'Tweet removed!'}, status=200)


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
    """
        id is required
        Action options are: like, unlike or retweet
    """
    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get('id')
        action = data.get('action')

        qs = Tweets.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "like":
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "unlike":
            obj.likes.remove(request.user)
            return Response(serializer.data, status=200)
        elif action == "retweet":
            # TODO
            pass
    return Response({}, status=200)
