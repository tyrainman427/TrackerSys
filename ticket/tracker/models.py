from django.db import models
import datetime
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from simple_history.models import HistoricalRecords


# Create your models here.
TICKET_STATUS = (
    ("Assigned","Assigned"),("Open","Open"),
    ("Pending","Pending"),("Closed","Closed"),("Canceled","Canceled"),
    ("Resolved","Resolved")
)

PRIORITY_STATUS = (
    ("Low","Low"),("Medium","Medium"),("High","High")
)

TICKET_TYPES = (
    ("Website","Website"),("IT Issue","IT Issue"),("HR Issue","HR Issue"),
    ("Password Help","Password Help"),("Purchase","Purchase"),("Mobile","Mobile"),
    ("Network","Network"),("Security","Security"),("Email","Email")
)

REGION = (
    ("Meriden","Meriden"),("North Haven","North Haven")
)

GROUPS = (
    ("Help Desk","Help Desk"),("Level 2","Level 2"),
    ("Level 3","Level 3"),("Web","Web"),("Security","Security"),
    ("Email","Email")
)

# Create your models here.
class TicketGroup(models.Model):
    name = models.CharField(max_length=30)
    user = models.ManyToManyField(User, blank=True)
    history = HistoricalRecords()

    def get_absolute_url(self):
        return reverse('tracker:group_detail', kwargs={'id': self.id})

    def __str__(self):
        return self.name


class Ticket(models.Model):
    name = models.CharField(max_length=50)
    title =models.CharField(max_length=100)
    region = models.CharField(max_length=50,choices=REGION)
    summary = models.TextField(max_length=300)
    type = models.CharField(max_length=100,choices=TICKET_TYPES)
    email =models.CharField(max_length=100)
    current_status = models.CharField(max_length=100,choices=TICKET_STATUS)
    created_at = models.DateField(auto_now_add=True)
    priority = models.CharField(max_length=10,choices=PRIORITY_STATUS)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        null=True, blank=True, on_delete=models.SET_NULL,related_name='added_by')
    history = HistoricalRecords()
    assigned = models.ForeignKey(TicketGroup,on_delete=models.CASCADE, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('tracker:ticket_detail', kwargs={'id': self.id})

    def was_published_recently(self):
        return self.created_at >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return "Incident: "+ self.title

    @property
    def _history_user(self):
        return self.added_by

    @_history_user.setter
    def _history_user(self, value):
        self.added_by = value

    def save_model(self, request, obj, form, change):
        if not obj.pk:
        # Only set added_by during the first save.
            obj.added_by = request.user
        super().save_model(request, obj, form, change)
