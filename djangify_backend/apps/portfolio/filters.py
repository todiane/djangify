# File: djangify_backend/apps/portfolio/filters.py

import django_filters
from django.db.models import Q
from djangify_backend.apps.portfolio.models import Portfolio


class PortfolioFilter(django_filters.FilterSet):
    technology = django_filters.CharFilter(method="filter_by_technology")
    date_from = django_filters.DateFilter(field_name="created_at", lookup_expr="gte")
    date_to = django_filters.DateFilter(field_name="created_at", lookup_expr="lte")
    search = django_filters.CharFilter(method="filter_by_search")

    class Meta:
        model = Portfolio
        fields = ["technology", "date_from", "date_to", "is_featured"]

    def filter_by_technology(self, queryset, name, value):
        return queryset.filter(technologies__slug=value)

    def filter_by_search(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value)
            | Q(description__icontains=value)
            | Q(short_description__icontains=value)
        )
