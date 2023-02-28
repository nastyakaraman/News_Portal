from django_filters import FilterSet, DateTimeFromToRangeFilter, CharFilter, ModelMultipleChoiceFilter
from django_filters.widgets import RangeWidget

from .models import Post, Category

class ProductFilter(FilterSet):

    time_in__range = DateTimeFromToRangeFilter(field_name='time_in',
                                               widget=RangeWidget(attrs={'type': 'datetime-local'}))

    heading__contains = CharFilter(field_name='heading',
                                   lookup_expr=' news')

    category__choice = ModelMultipleChoiceFilter(field_name='category', queryset=Category.objects.all(), label='По категории')

