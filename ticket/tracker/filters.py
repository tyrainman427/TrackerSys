import django_filters
from .models import *

class TicketFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Ticket
        fields = ['name','current_status', 'priority','assigned']
    
