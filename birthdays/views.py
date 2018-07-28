# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, redirect, render
# from django.core.urlresolvers import reverse_lazy
from django.urls import reverse_lazy
from .forms import InvitationForm, EventForm, PersonForm, EventDetailForm
from django.views.generic import ListView, DetailView, \
    CreateView, UpdateView, DeleteView
from .models import Event, Invitation, Person
from django.utils import timezone
import datetime
from django.views.generic.edit import ModelFormMixin
from birthdays import functions
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect

sixty_days_into_the_future = timezone.now().date() + datetime.timedelta(days=90)

class IndexView(ListView):
    template_name = 'index.html'
    context_object_name = 'upcoming_events'

    def get_queryset(self):
        pass

    #The following override allows you to include multiple query sets on a page/template.
    #Below I only added 'upcoming...', but feel free to add more as required.
    def get_context_data(self, *args, **kwargs):
        all_persons = Person.objects.all()
        all_events = Event.objects.all()
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        context['upcoming_events'] = functions.get_upcoming_events(all_events)
        context['upcoming_birthdays'] = functions.get_upcoming_birthdays(all_persons)
        context['active_invitations'] = functions.get_active_invitations()
        context['past_events'] = functions.get_past_events()
        return context


class InvitationsView(ListView):
    model = Invitation
    template_name = 'invitations.html'


class InvitationDetailView(DetailView):
    print("in InvitationDetailView()")
    model = Invitation
    template_name = 'invitation_detail.html'
    context_object_name = 'invitation'


class InvitationUpdateView(UpdateView):
    model = Invitation
    fields = ('id', 'response')
    form = InvitationForm()


class InvitationDeleteView(DeleteView):
    model = Invitation
    success_url = reverse_lazy('index')


class EventListView(ListView):
    model = Event
    template_name = 'event_list.html'
    context_object_name = 'all_events'

    def get_queryset(self):
        all_events = Event.objects.all()
        return all_events


class EventDetailView(DetailView):
    model = Event
    template_name = 'event_detail.html'
    # context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['event'] = get_object_or_404(Event, pk=pk)
        context['invitees'] = Invitation.objects.filter(event_id=pk)
        context['yes_responses'] = functions.get_yes_responses(pk) # Invitation.objects.filter(event_id=pk) #.filter(response='Yes')
        context['no_responses'] = functions.get_no_responses(pk)
        return context


class EventCreateView(CreateView):
    model = Event
    fields = ('id','title','event_dt','invitation_text', 'invitees')

    def form_valid(self, form):
        s = form.save(commit=False)
        s.save()
        for person in form.cleaned_data['invitees']:
            created = Invitation.objects.get_or_create(event=form.instance,
                                       person=person,
                                       response='undecided')
            if created:
                functions.send_email(self, person)
            else:
                print(person.name + ' was already invited.')
        return super(ModelFormMixin, self).form_valid(form)


class EventUpdateView(UpdateView):
    model = Event
    fields = ('id','title','event_dt','invitation_text', 'invitees')

    def form_valid(self, form):
        print("In EventUpdateView()")
        self.object = form.save(commit=False)
        self.object.save()
        for person in form.cleaned_data['invitees']:
            obj, created = Invitation.objects.get_or_create(person_id=person.id,
                                             event=self.object,
                                             response='undecided')
            if created:
                invitation_pk = str(obj.pk)
                print(invitation_pk)
                functions.send_email(self, obj)
            else:
                print(str(Person.name) + " was already invited.")

        return super(ModelFormMixin, self).form_valid(form)


class EventDeleteView(DeleteView):
    model = Event
    success_url = reverse_lazy('event_list')


class PersonListView(ListView):
    model = Person
    template_name = 'person_list.html'
    context_object_name = 'all_persons'

    def get_queryset(self):
        all_persons = Person.objects.all()
        return all_persons


class PersonDetailView(DetailView):
    print("in PersonDetailView()")
    model = Person
    template_name = 'person_detail.html'
    context_object_name = 'person'


class PersonCreateView(CreateView):
    model = Person
    fields = ('id', 'name', 'email', 'birth_dt')


class PersonUpdateView(UpdateView):
    model = Person
    print("In PersonUpdateView()")
    fields = ('id', 'name', 'email', 'birth_dt')


class PersonDeleteView(DeleteView):
    model = Person
    success_url = reverse_lazy('person_list')

# function-based views
# def person_detail(request, pk):
#     person = get_object_or_404(Person, pk=pk)
#     return render(request, 'person_detail.html', {'person': person})
#
# def person_edit(request, pk):
#     person = get_object_or_404(Person, pk=pk)
#     if request.method == "POST":
#         form = PersonForm(request.POST, instance=person)
#         if form.is_valid():
#             person = form.save(commit=False)
#             person.created_by = request.user
#             person.created_dt = timezone.now()
#             person.save()
#             return redirect('person', pk=person.pk)
#     else:
#         form = PersonForm(instance=person)
#     return render(request, 'person_edit.html', {'form': form})
#
# def person_new(request):
#     if request.method == "POST":
#         form = PersonForm(request.POST)
#         if form.is_valid():
#             person = form.save(commit=False)
#             person.created_by = request.user
#             person.created_dt = timezone.now()
#             person.save()
#             return redirect('person_detail', pk=person.pk)
#     else:
#         form = PersonForm()
#
#     return render(request, 'person_edit.html', {'form': form})
#
# def event_detail(request, pk):
#     event = get_object_or_404(Event, pk=pk)
#     form = EventDetailForm()
#     invitations = Invitation.objects.filter(event_id=pk)
#     for invitation in invitations:
#         print(invitation)
#     return render(request, 'event_detail.html', {'event': event})
#
# def event_edit(request, pk):
#     event = get_object_or_404(Event, pk=pk)
#     if request.method == "POST":
#         form = EventForm(request.POST)
#         if form.is_valid():
#             event = form.save(commit=False)
#             event.created_by = request.user
#             event.created_dt = timezone.now()
#             event.save()
#             for person in form['Add more persons: ']:
#                 print(person)
#             return redirect('event_detail', pk=event.pk)
#     else:
#         form = EventForm(instance=event)
#         for invitees in form['Current Invitees: ']:
#             print(invitees)
#     return render(request, 'event_edit.html', {'form': form})
#
# def event_new(request):
#     if request.method == "POST":
#         form = EventForm(request.POST)
#         if form.is_valid():
#             event = form.save(commit=False)
#             event.created_by = request.user
#             event.created_dt = timezone.now()
#             event.save()
#             return redirect('event_detail', pk=event.pk)
#     else:
#         form = EventForm()
#
#     return render(request, 'event_edit.html', {'form': form})