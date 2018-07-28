# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from birthdays.models import Event, Person, Invitation

# Register your models here.
admin.site.register(Event)
admin.site.register(Person)
admin.site.register(Invitation)