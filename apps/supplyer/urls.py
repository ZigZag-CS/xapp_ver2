from django.urls import path, re_path

from apps.supplyer.views import *



app_name = "supplyer"

urlpatterns = [

    path('home/', AccountHomeView.as_view(), name='dashboard-home'),

    # path('details/', user.UserDetailUpdateView.as_view(), name='user-update'),
    #
    # re_path(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/$', user.AccountEmailActivateView.as_view(), name='email-activate'),
    #
    # path('email/resend-activation/', user.AccountEmailActivateView.as_view(), name='resend-activation'),
]