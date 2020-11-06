from posts.models import UserPost

import django_filters

class Search(django_filters.FilterSet):
    artist=django_filters.CharFilter(field_name='artist',lookup_expr='icontains')
    
    class Meta:
        model=UserPost
        fields=['artist']