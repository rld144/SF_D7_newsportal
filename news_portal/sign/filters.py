from django_filters import FilterSet, ModelMultipleChoiceFilter
from newsportal.models import Category


class CatFilter(FilterSet):

    filter = ModelMultipleChoiceFilter(
        field_name='name',
        queryset=Category.objects.all(),
        label='',
    )

