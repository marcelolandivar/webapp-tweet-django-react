from django.contrib import admin

from .models import Tweets


class TweetsAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'user')
    search_fields = ['content', 'user__username', 'user__email']

    class Meta:
        model = Tweets
# Filtering in the user model is using __ Ex: user__username
# __str__ in the model and in the list display to show in the admin site


admin.site.register(Tweets, TweetsAdmin)
