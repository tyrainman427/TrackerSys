from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Ticket, TicketUser
from .forms import TicketForm
from django.contrib.auth.decorators import permission_required
import csv, io
# from braces.views import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
import operator
from functools import reduce
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView

# Create your views here.

def dashboard(request):
    tickets = Ticket.objects.all()
    users = User.objects.all()
    ticket_count = tickets.count()
    user_tickets = Ticket.objects.all().filter(added_by=request.user)
    open_tickets = Ticket.objects.filter(current_status__contains='Open')
    high_priority_tickets = Ticket.objects.filter(priority__contains='High')
    paginator = Paginator(tickets, 5)
    # get the page parameter from the query string
    # if page parameter is available get() method will return empty string ''
    page = request.GET.get('page')

    try:
        # create Page object for the given page
        tickets = paginator.page(page)
    except PageNotAnInteger:
        # if page parameter in the query string is not available, return the first page
        tickets = paginator.page(10)
    except EmptyPage:
        # if the value of the page parameter exceeds num_pages then return the last page
        tickets = paginator.page(paginator.num_pages)

    context = {
        'tickets':tickets,
        'users':users,
        'open_tickets':open_tickets,
        'high_priority_tickets':high_priority_tickets,
        'user_tickets':user_tickets,
        'ticket_count':ticket_count,
    }
    return render(request, 'tracker/dashboard.html',context)

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


class TicketListView(ListView):
    model = Ticket
    # user_list = User.objects.all()
    queryset = Ticket.objects.all()#order_by('-created_at').filter(current_status__contains='Assigned')
    paginate_by = 5

    def get_queryset(self):
        result = super(TicketListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(title__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(priority__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(name__icontains=q) for q in query_list))
            )

        return result

class TicketDetailView(DetailView):
    template_name = "tracker/ticket_detail.html"
    userAdmin = User.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Ticket, id=id_)

class TicketUpdate(UpdateView):
    template_name = "tracker/ticket_create.html"
    form_class = TicketForm
    queryset = Ticket.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Ticket, id=id_)

    def form_valid(self,form):
        return super().form_valid(form)

class TicketDeleteView(DeleteView):
    model = Ticket
    success_url = '/tracker/'


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
