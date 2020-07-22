from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from tracker.models import Ticket, TicketGroup, HistoricalTicket

# Register your models here.
class TicketHistoryAdmin(SimpleHistoryAdmin):
    list_display = ["id", "title", "current_status"]
    history_list_display = ["title","current_status"]
    search_fields = ['name',]


admin.site.register(Ticket,TicketHistoryAdmin)
admin.site.register(TicketGroup,SimpleHistoryAdmin)
admin.site.register(HistoricalTicket)
