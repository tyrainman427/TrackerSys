from django.urls import path
from . import views
from .filters import TicketFilter
from .views import (TicketCreateView,onboarding, TicketDetailView,
 TicketListView,TechView, TicketUpdate, ticket_upload, dashboard,
 GroupCreateView,GroupUpdateView,GroupDeleteView,GroupDetailView
 )
from users.views import profile

app_name = 'tracker'

urlpatterns = [
    path('tickets/', views.TicketListView.as_view(), name='ticket-list'),
    path('', views.dashboard, name='index'),
    path('<int:id>/', views.TicketDetailView.as_view(), name='ticket_detail'),
    path('tracker/create/', views.TicketCreateView.as_view(), name="ticket-create"),
    path('users/', views.get_users, name='get-users'),
    path('<int:id>/update/', views.TicketUpdate.as_view(), name='ticket-update'),
    path('<int:pk>/delete/', views.TicketDeleteView.as_view(), name='ticket-delete'),
    path('upload-csv/', views.ticket_upload, name='ticket_upload'),
    path('tech_update/', views.TechView.as_view(), name='tech_update'),
    path('onboarding/', views.onboarding,name='onboarding'),
    path('create_group/', views.GroupCreateView.as_view(), name='group_create'),
    path('group/', views.GroupListView.as_view(), name='group-list'),

    path('group/<int:id>/', views.GroupDetailView.as_view(), name='group_detail'),
    path('group/<int:id>/group_update/', views.GroupUpdateView.as_view(), name='group-update'),
    path('group/<int:pk>/group_delete/', views.GroupDeleteView.as_view(), name='group_delete'),
    path('users/profile/', profile,name='profile')

]

urlpatterns += [

]
