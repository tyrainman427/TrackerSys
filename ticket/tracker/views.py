from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Ticket, TicketGroup
from .forms import *
from django.contrib.auth.decorators import permission_required,login_required
import csv, io
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
import operator
from functools import reduce
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from .filters import TicketFilter

# Create your views here.

@login_required
def dashboard(request):
    tickets = Ticket.objects.all()
    ticket_count = Ticket.objects.all()
    users = User.objects.all()
    user_tickets = Ticket.objects.all().filter(added_by=request.user)
    open_tickets = Ticket.objects.filter(current_status__contains='Open')
    high_priority_tickets = Ticket.objects.filter(priority__contains='High')
    paginator = Paginator(tickets, 5)
    # get the page parameter from the query string
    # if page parameter is available get() method will return empty string ''
    page = request.GET.get('page')
    myFilter = TicketFilter(request.GET, queryset=tickets)
    tickets = myFilter.qs

    # tiks = len(high_priority_tickets)
    # tic_count = len(ticket_count)
    # open = len(open_tickets)
    #
    # tik_count_percent = 0
    # open_tik_percent = 0
    # if tiks > 0:
    #     tik_count_percent = int((100/tic_count) * (tiks/100) * 100)
    #     open_tik_percent = int((100/tic_count) * (open/100) * 100)
    #     print("Ticket Percentage: ",tik_count_percent)


    context = {
        'tickets':tickets,
        'ticket_count':ticket_count,
        'users':users,
        'open_tickets':open_tickets,
        'high_priority_tickets':high_priority_tickets,
        'user_tickets':user_tickets,
        'filter': myFilter,
        # 'history': history,
        # 'tik_count_percent': tik_count_percent,
        # 'open_tik_percent': open_tik_percent
    }
    return render(request, 'tracker/dashboard.html',context)

def onboarding(request):
    return render(request,'tracker/onboarding.html',{})

class TicketCreateView(CreateView):
    template_name = "tracker/ticket_create.html"
    form_class = TicketForm
    queryset = Ticket.objects.all()

    def form_valid(self,form):
        form.instance.added_by = self.request.user
        self.object = form.save(commit=False)
        self.object.current_status = "Open"
        self.object.save()


        return super().form_valid(form)


class GroupCreateView(CreateView):
    template_name = "tracker/group_create.html"
    form_class = GroupForm
    queryset = TicketGroup.objects.all()


    def form_valid(self,form):
        form.instance.added_by = self.request.user
        self.object = form.save(commit=False)
        self.object.save()
        self.success_message = "Your group has been created!"

        return super().form_valid(form)

class GroupDetailView(DetailView):
    template_name = "tracker/group_detail.html"
    groups = TicketGroup.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(TicketGroup, id=id_)

class GroupUpdateView(UpdateView):
    template_name = "tracker/group_create.html"
    form_class = GroupForm
    queryset = TicketGroup.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(TicketGroup, id=id_)

    def form_valid(self,form):
        return super().form_valid(form)

class GroupDeleteView(DeleteView):
    model = TicketGroup
    success_url = '/group/'

class GroupListView(ListView):
    model = TicketGroup
    template_name = "tracker/ticketgroup_list.html"
    queryset = TicketGroup.objects.all()
    paginate_by = 5


class TicketListView(ListView):
    model = Ticket
    template_name = "tracker/ticket_list.html"
    # user_list = User.objects.all()
    queryset = Ticket.objects.all()#order_by('-created_at').filter(current_status__contains='Assigned')
    paginate_by = 5


class TicketDetailView(DetailView):
    template_name = "tracker/ticket_detail.html"
    queryset = Ticket.objects.all()
    history = Ticket.history.all()
    form_class = TechForm

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Ticket, id=id_)

    def form_valid(self,form):
        return super().form_valid(form)

class TicketUpdate(UpdateView):
    template_name = "tracker/ticket_create.html"
    form_class = TechForm
    queryset = Ticket.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Ticket, id=id_)

    def form_valid(self,form):
        return super().form_valid(form)

class TechView(ListView):
    model = Ticket
    template_name = "tracker/tech_view.html"
    queryset = Ticket.objects.all()
    paginate_by = 10


class TicketDeleteView(DeleteView):
    model = Ticket
    success_url = '/'

def ticket_closed(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TicketResolveForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            tick = Ticket(name=name,email=email,title=title,summary=summary,submitter= submitter,)
            tick.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/tracker/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TicketForm()

    return render(request, 'tracker/ticket_form.html', {'form': form})


@permission_required('admin.can_add_log_entry')
def ticket_upload(request):
    template = 'tracker/ticket_upload.html'

    prompt = {
        'order':'Order of the CVS >>'
    }
    if request.method == 'GET':
        return render(request, template, prompt)

    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, "this is not a csv file")

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',',quotechar="|"):
        _, created = Ticket.objects.update_or_create(
            name=column[1],
            title=column[2],
            summary=column[3],
        )
    context = {}
    return render(request,template, context)

def get_users(request):
    users = User.objects.all()
    return render(request, 'tracker/user_list.html',{"users":users})


def get_ticket(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TicketForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            title = form.cleaned_data['title']
            summary = form.cleaned_data['summary']
            submitter = form.cleaned_data['submitter']
            tick = Ticket(name=name,email=email,title=title,summary=summary,submitter= submitter,)
            tick.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/tracker/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TicketForm()

    return render(request, 'tracker/ticket_form.html', {'form': form})
