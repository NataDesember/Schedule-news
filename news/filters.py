from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'time_in': ['gt'],
            'author': ['exact'],
            'categorys': ['exact']
        }