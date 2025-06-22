from .models import Profile,Transaction
import django_filters
from django.db.models import Q

class TransactionFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(field_name='status',choices=Transaction.STATUS_CHOICE)
    transaction_type = django_filters.ChoiceFilter(field_name='transaction_type',choices=Transaction.TRANSACTION_TYPE)
    class Meta:
        model = Transaction
        fields = ['status','transaction_type']

class ProfileFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_by_full_name')
    email = django_filters.CharFilter(field_name='email',lookup_expr='icontains')
    phonenumber = django_filters.CharFilter(field_name='phonenumber',lookup_expr='icontains')
    account_number = django_filters.CharFilter(field_name='account__account_number',lookup_expr='icontains')
    class Meta:
        method = Profile
        fields = ['name','email','phonenumber','account_number']

    def filter_by_full_name(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value)|Q(last_name__icontains=value)
        )