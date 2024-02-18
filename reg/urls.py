from . import views
from django.urls import path
# from .views import reverse_rsvp

urlpatterns = [
    path('',views.home, name='home' ),
    path('logout',views.logout_user, name='logout' ),
    path('register',views.reg_user, name='register' ),
    path('event/<int:pk>',views.events, name='events'),
    path('delete_event/<int:pk>',views.delete_events, name='delete_events'),
    path('update_event/<int:pk>',views.update_event, name='update_event'),
    path('add_event',views.add_event, name='add_event'),
    path('RSVP/<int:pk>',views.RSVP, name='RSVP'),
    path('search/', views.search_events, name='search_events'),
    # path('reverse_rsvp/<int:pk>', reverse_rsvp, name='reverse_rsvp'),
]
