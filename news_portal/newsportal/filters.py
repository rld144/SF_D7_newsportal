from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'header': ['icontains'],
            'text': ['icontains'],
            'date': ['date__gt'],
            'categories': ['exact'],
    }