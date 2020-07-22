from django import forms
from .models import *
import datetime
from django.utils import timezone
from django.contrib.auth.models import User


TICKET_STATUS = (
    ("Assigned","Assigned"),("Open","Open"),("Pending","Pending"),("Closed","Closed")
)
RESOLVE_TYPES = (
    ("Resolved","Resolved"),("Re-Open","Re-Open"),("Cancelled","Cancelled"),("Vendor Resolved","Vendor Resolved")
)

PRIORITY_STATUS = (
    ("Low","Low"),("Medium","Medium"),("High","High")
)

class GroupForm(forms.ModelForm):
    name = forms.CharField(max_length=100)

    class Meta:
        model = TicketGroup
        fields = ("name",)

class TicketResolveForm(forms.ModelForm):
    reason_for_closing = forms.CharField(max_length=500)
    resolve_status = forms.ChoiceField(choices=RESOLVE_TYPES)

    class Meta:
        model = Ticket
        fields = "__all__"

class TicketForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    region = forms.ChoiceField(choices=REGION)
    type = forms.ChoiceField(choices=TICKET_TYPES)
    title = forms.CharField(max_length=100)
    summary = forms.CharField(widget=forms.Textarea)
    priority = forms.ChoiceField(choices=PRIORITY_STATUS,required=False)
    # assigned = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True), empty_label=None)

    class Meta:
        model = Ticket
        fields = "__all__"
        exclude = ('added_by','email','assigned','current_status','ticket_id')


class TechForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    region = forms.ChoiceField(choices=REGION)
    type = forms.ChoiceField(choices=TICKET_TYPES)
    title = forms.CharField(max_length=100)
    summary = forms.CharField(widget=forms.Textarea)
    priority = forms.ChoiceField(choices=PRIORITY_STATUS,required=False)
    # assigned = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True), empty_label=None)

    class Meta:
        model = Ticket
        fields = "__all__"
        exclude = ('added_by','email','ticket_id')
