from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),                        #Index
    url(r'^events/$', views.EventListView.as_view(), name='event_list'),
    url(r'^event/create/$', views.EventCreateView.as_view(), name='event_create'),
    url(r'^event/(?P<pk>\d+)/$', views.EventDetailView.as_view(), name='event_detail'),
    url(r'^event/edit/(?P<pk>\d+)/$', views.EventUpdateView.as_view(), name='event_update'),
    url(r'^event/delete/(?P<pk>\d+)/$', views.EventDeleteView.as_view(), name='event_delete'),
    url(r'^persons/$', views.PersonListView.as_view(), name='person_list'),
    url(r'^person/(?P<pk>\d+)/$', views.PersonDetailView.as_view(), name='person_detail'),
    url(r'^person/create/$', views.PersonCreateView.as_view(), name='person_create'),
    url(r'^person/edit/(?P<pk>\d+)/$', views.PersonUpdateView.as_view(), name='person_update'),
    url(r'^person/delete/(?P<pk>\d+)/$', views.PersonDeleteView.as_view(), name='person_delete'),
    url(r'^invitation/edit/(?P<pk>\d+)/$', views.InvitationUpdateView.as_view(), name='invitation_update'),
    url(r'^invitation/(?P<pk>\d+)/$', views.InvitationDetailView.as_view(), name='invitation_detail'),
    url(r'^invitation/delete/(?P<pk>\d+)/$', views.InvitationDeleteView.as_view(), name='invitation_delete'),
    # url(r'^add_invitees$', views.add_invitees, name='add_invitees'),

]