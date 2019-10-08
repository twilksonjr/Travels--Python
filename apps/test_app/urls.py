from django.conf.urls import url
from . import views
                    
urlpatterns = [
    # render routes
    url(r'^$', views.Index),
    url(r'^registration$', views.Registration),
    url(r'^login$', views.Login),
    url(r'^dashboard$', views.Dashboard),
    url(r'^trip$', views.Trip),
    url(r'^edit_trip/(?P<trip_id>\d+)$', views.Edit_trip),
    url(r'^read/(?P<trip_id>\d+)$', views.Read),


    # process routes
    url(r'^update_trip/(?P<trip_id>\d+)$', views.Update_trip),
    url(r'^create_trip$', views.Create_trip),
    url(r'^delete_trip/(?P<trip_id>\d+)$', views.Delete_trip),
    url(r'^logout$', views.Logout),
]