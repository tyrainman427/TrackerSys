from django.urls import path
from . import views
from .views import TicketCreateView, TicketDetailView, TicketListView, TicketUpdate, ticket_upload, dashboard

app_name = 'tracker'

urlpatterns = [
    path('tickets/', views.TicketListView.as_view(), name='ticket-list'),
    path('', views.dashboard, name='index'),
    path('<int:id>/', views.TicketDetailView.as_view(), name='detail'),
    path('create/', views.TicketCreateView.as_view(), name="ticket-create"),
    #path('ticket_form/', views.get_ticket, name='get-ticket'),
    path('<int:id>/update/', views.TicketUpdate.as_view(), name='ticket-update'),
    path('<int:pk>/delete/', views.TicketDeleteView.as_view(), name='ticket-delete'),
    path('upload-csv/', views.ticket_upload, name='ticket_upload'),
]

urlpatterns += [

]
