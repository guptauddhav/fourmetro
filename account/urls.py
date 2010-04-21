from django.conf.urls.defaults import *

from account import views

urlpatterns = patterns('',
    #(r'^dashboard/$', views.dashboard),
    #(r'^login/$', views.login),
    #(r'^logout/$', views.logout),
    (r'^register/$', views.register),
    #(r'^password-change/$', views.request_password_change),
    (r'^email-sent/$', 'django.views.generic.simple.direct_to_template', {'template': 'account/email_sent.html'}),
    #(r'^c/$', views.confirm_email),
    #(r'^r/$', views.password_reset),
)
