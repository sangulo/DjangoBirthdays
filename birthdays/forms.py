from django import forms
from django.forms import inlineformset_factory
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from .models import Event, Person, Invitation

# class BaseInvitationFormset(BaseInlineFormSet):
#
#     def add_fields(self, form, index):
#         super(BaseInvitationFormset, self).add_fields(form, index)
#
#     def is_valid(self):
#         result = super(BaseInvitationFormset, self).is_valid()
#         if self.is_bound:
#             for form in self.forms:
#                 if hasattr(form, 'nested'):
#                     result = result and form.nested.is_valid()
#         return result
#
#     def save(self, commit=True):
#         result = super(BaseInvitationFormset, self).save(commit=commit)
#         for form in self.forms:
#             if hasattr(form, 'nested'):
#                 if not self._should_delete_form(form):
#                     form.nested.save(commit=commit)
#         return result

# InvitationFormset = inlineformset_factory(Event, Invitation, formset=BaseInvitationFormset, extra=1)

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('id','title','event_dt','invitation_text')#,'invitations') #'guest_of_honor' ToDO: get to this later

    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user', '')
    #     print('Entering EventForm __init__()')
    #     print("User: " + str(user))
    #     super(EventForm, self).__init__(*args, **kwargs)
    #     if kwargs.get('instance'):
    #         event_id = kwargs['instance'].id
    # #         invitations = Invitation.objects.filter(event_id=event_id)
    # #         for invitees in invitations:
    # #             print("Invited: " + str(invitees))
    #
    #     # invitation_set = forms.ModelMultipleChoiceField()
    #     # self.fields['invitations:'] = forms.ModelMultipleChoiceField(Person.objects.all(),
    # #                                              required=False,
    # #                                              widget=forms.SelectMultiple())
    #     self.fields['Current Invitees: '] = \
    #         forms.ModelChoiceField(Invitation.objects.filter(event_id=event_id),
    #                                                                required=False)
    #     self.fields['Add more persons: '] = forms.ModelChoiceField(queryset=Person.objects.all(),
    #                                                                widget=forms.SelectMultiple,
    #                                                                required=False)

        # print('Leaving EventForm __init__()')

class EventDetailForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('id','title','event_dt', 'invitation_text')

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('id','name','email','birth_dt')

class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ('id', 'response')


    # def __init__(self, *args, **kwargs):
    #    # model = Invitation
    #    super(InvitationForm, self).__init__(*args, **kwargs)
    #    self.fields['event'].widget.attrs['readonly'] = True
    #    self.fields['person'].widget.attrs['readonly'] = True

# class CustomGuestsField(forms.Field):
#
#     def clean(self):
#         return self
#
#     def __init__(self, *args, **kwargs):
#         if kwargs.get('instance'):
#             event_id = kwargs['instance'].id
