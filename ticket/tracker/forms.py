from django import forms
from .models import Ticket
import datetime
from django.utils import timezone


TICKET_STATUS = (
    ("Assigned","Assigned"),("Open","Open"),("Pending","Pending"),("Closed","Closed")
)

PRIORITY_STATUS = (
    ("Low","Low"),("Medium","Medium"),("High","High")
)

class TicketForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)
    title = forms.CharField(max_length=100)
    summary = forms.CharField(widget=forms.Textarea)
    priority = forms.ChoiceField(choices=PRIORITY_STATUS,required=False)


    class Meta:
        model = Ticket
        fields = "__all__"
        exclude = ('added_by','current_status')
