from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Ticket
from .forms import TicketForm
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.generic import DetailView, ListView, UpdateView, CreateView

# Create your views here.
class TicketCreateView(CreateView):
    template_name = "tracker/ticket_create.html"
    form_class = TicketForm
    queryset = Ticket.objects.all()

    def form_valid(self,form):
        return super().form_valid(form)


class TicketListView(ListView):
    model = Ticket
    queryset = Ticket.objects.order_by('-created_at').filter(current_status__contains='Open')

class TicketDetailView(DetailView):
    template_name = "tracker/ticket_detail.html"

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
