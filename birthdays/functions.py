from __future__ import unicode_literals
from django.http import HttpResponse
from .models import Event, Invitation
from django.utils import timezone
import datetime
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError

sixty_days_into_the_future = timezone.now().date() + datetime.timedelta(days=90)


########### Functions ##################
def send_email(self, Invitation):
    try:
        print('sending email invite to: ' + Invitation.person.name)
        # send_mail("You're invited to " + Invitation.event.title,
        #         Invitation.event.invitation_text + '  '
        #         'RSVP by copying the following URL into your web browser:  ' +
        #             '127.0.0.1:8000/birthdays/invitation/' +
        #             str(Invitation.pk) + '/',
        #         'sangulo@austin.utexas.edu', #from_email
        #         [Invitation.person.email], fail_silently=False)
        subject = "You're invited to " + Invitation.event.title
        message = (Invitation.event.invitation_text + '  '
                    'RSVP by copying the following URL into your web browser:  ' +
                    '127.0.0.1:8000/birthdays/invitation/' +
                    str(Invitation.pk) + '/')
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, settings.ADMINS)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')


def get_active_invitations():
    print('in get_active_invitations')
    return (Invitation.objects.filter(event__event_dt__gte=timezone.now()).order_by('event'))


def get_upcoming_events(all_events):
    upcoming_events = []
    print("get_upcoming_events()")
    for event in all_events:
        if timezone.now().date() <= event.event_dt.date() < sixty_days_into_the_future:
            upcoming_events.append(event)

    return upcoming_events

def get_past_events():
    past_events = Event.objects.filter(event_dt__lt=timezone.now().date()).order_by('-event_dt')
    return past_events

def get_upcoming_birthdays(all_persons):
    print('get_upcoming_birthdays()')
    persons = []
    for person in all_persons:
        current_year_birthday = person.birth_dt.replace(year = timezone.now().year)
        if current_year_birthday < timezone.now().date():
            next_birthday = current_year_birthday.replace(year = current_year_birthday.year + 1)
        else:
            next_birthday = current_year_birthday

        if next_birthday < sixty_days_into_the_future:
            persons.append(person)

    return persons

def get_yes_responses(event_pk):
    # yes_resonses = []
    return  Invitation.objects.filter(event__pk=event_pk).filter(response__iexact='YES')

def get_no_responses(event_pk):
    return Invitation.objects.filter(event__pk=event_pk).filter(response__iexact='NO')

def add_invitees(request, invitee):
    print("hello from add_invitees()")
