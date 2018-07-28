# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.urlresolvers import reverse


class Person(models.Model):
    name = models.CharField(max_length=50)
    # email = models.CharField(max_length=50, default='')
    email = models.EmailField()
    birth_dt = models.DateField(null=True)
    created_dt = models.DateTimeField(default=timezone.now)
    created_by = ""  # TODO: get handle on current user (person adding event)

    def __str__(self):
        return self.name #+ ', id ' + str(self.id)

    def upcoming_birthday(self):
        return timezone.now() <= self.birth_dt #TODO: needs to see if birthday is under 30 days from now.  Do not compare year

    def save(self, *args, **kwargs):
            super(Person, self).save(*args, **kwargs)  # Call the "real" save() method.

    def get_absolute_url(self):
        return reverse('person_detail', kwargs={'pk': self.pk})

class Event(models.Model):
    created_dt = models.DateTimeField(default=timezone.now)
    created_by = "" #TODO: get handle on current user (person adding event)
    title = models.CharField(max_length=100, default="Title")
    invitation_text = models.TextField()
    event_dt = models.DateTimeField(blank=False, null=False)
    invitees = models.ManyToManyField(Person, through='Invitation')
    # guest_of_honor = models.ForeignKey('Person') Todo: do this

    # def upcoming_event(self):
    #     return timezone.now() + datetime.timedelta(days=30) >= self.event_dt >= timezone.now()
    # upcoming_event.admin_order_field = event_dt
    # upcoming_event.boolean = True
    # upcoming_event.short_description = "Upcoming event?"

    def invitations_sent(self):
        return self.invitation_set.filter(response='yes')

    def save(self, *args, **kwargs):
            super(Event, self).save(*args, **kwargs)  # Call the "real" save() method.

    def __str__(self):
        return self.title + " " + str(self.event_dt)

    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'pk': self.pk})

# class InvitationManager(models.Manager):
#     def active_invitations(self):
#         print(str(timezone.now()) + 'is the time in Invitation.active_invitations()')
#         return Invitation.objects.filter(event__event_dt__gte=timezone.now())

class Invitation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    response = models.CharField(max_length=9)#TODO:  consider making this an enumerater (YES='yes', NO='no', UNDECIDED='')
    # objects = InvitationManager()

    def __str__(self):
        return self.person.name +  ' ' + self.response + ' '  + self.event.title

    def save(self, *args, **kwargs):
            super(Invitation, self).save(*args, **kwargs)  # Call the "real" save() method.

    def get_absolute_url(self):
        return reverse('invitation_detail', kwargs={'pk': self.pk})

# class GuestOfHonor(models.Model):
#     event = models.ForeignKey(Event)
#     person = models.ForeignKey(Person)
#
#     def __str__(self):
#         return self.person.name
