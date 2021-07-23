from django.http import JsonResponse
from django.conf.global_settings import ALLOWED_HOSTS
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
import random
from django.conf import settings
from .forms import TweetForm
from .models import Tweets


ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home(request, *args, **kwargs):
    return render(request, 'tweets/index.html', context={}, status=200)


def tweet_create_view(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        # Do form logic
        obj.user = request.user or None
        obj.save()
        # If it is a AJAX response then we do not need to redirect
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)
            # 201 == created_items
        if is_safe_url(next_url, ALLOWED_HOSTS) and next_url != None:
            redirect(next_url)
        form = TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={"form": form})


def tweet_list_view(request, *args, **kwargs):
    qs = Tweets.objects.all()
    tweets_list = [x.serialize() for x in qs]
    data = {
        "isUser": False,
        "response": tweets_list
    }
    return JsonResponse(data)


def tweet_detail_view(request, tweet_id, *args, **kwargs):
    """
    REST API VIEW
    Consume by JS
    return JSON
    """
    data = {
        "id": tweet_id,
        # "image_path": obj.image
    }
    status = 200
    try:
        obj = Tweets.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data["message"] = "Not Found"
        status = 404

    return JsonResponse(data, status=status)
