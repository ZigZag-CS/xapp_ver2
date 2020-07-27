from django.urls import path, re_path

from apps.customer.views import *



app_name = "customer"

urlpatterns = [

    path('home/', AccountHomeView.as_view(), name='customer-dashboard-home'),

    path('profile/', CustomerDetailUpdateView.as_view(), name='customer-update'),
    path('profile1/', CustomerDetailUpdateView1.as_view(), name='customer-update1'),

    # re_path(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/$', user.AccountEmailActivateView.as_view(), name='email-activate'),

    # path('email/resend-activation/', user.AccountEmailActivateView.as_view(), name='resend-activation'),

]