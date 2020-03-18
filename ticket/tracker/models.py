from django.db import models
import datetime
from django.contrib.auth.models import User 
from django.utils import timezone
from django.urls import reverse

# Create your models here.
TICKET_STATUS = (
    ("Assigned","Assigned"),("Open","Open"),("Pending","Pending"),("Closed","Closed")
)

PRIORITY_STATUS = (
    ("Low","Low"),("Medium","Medium"),("High","High")
)

# Create your models here.
class Ticket(models.Model):
    incident_num = models.CharField(max_length=5)
    name = models.CharField(max_length=100)
    email =models.CharField(max_length=100)
    title =models.CharField(max_length=100)
    summary = models.TextField(max_length=300)
    current_status = models.CharField(max_length=10,choices=TICKET_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=10,choices=PRIORITY_STATUS)
    submitter = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('tracker:detail', kwargs={'id': self.id})

    def was_published_recently(self):
        return self.created_at >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return "Incident:" + self.incident_num + " " + self.title

class TicketUser(models.Model):
    is_admin = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE)
