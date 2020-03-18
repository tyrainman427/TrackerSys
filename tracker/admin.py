from django.contrib import admin
from tracker.models import Ticket, TicketUser

# Register your models here.
admin.site.register(Ticket)
admin.site.register(TicketUser)
