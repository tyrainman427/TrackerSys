from django.db import models
import datetime
from django.contrib.auth.models import User
from django.conf import settings
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
    name = models.CharField(max_length=100)
    title =models.CharField(max_length=100)
    summary = models.TextField(max_length=300)
    email =models.CharField(max_length=100)
    current_status = models.CharField(max_length=10,choices=TICKET_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=10,choices=PRIORITY_STATUS)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        null=True, blank=True, on_delete=models.SET_NULL)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)


    def get_absolute_url(self):
        return reverse('tracker:ticket_detail', kwargs={'id': self.id})

    def was_published_recently(self):
        return self.created_at >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return "Incident: "+ self.title

    def save_model(self, request, obj, form, change):
        if not obj.pk:
        # Only set added_by during the first save.
            obj.added_by = request.user
        super().save_model(request, obj, form, change)

class TicketUser(models.Model):
    is_admin = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)
