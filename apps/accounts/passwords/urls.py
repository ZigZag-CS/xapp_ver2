# accounts.passwords.urls.py
from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from apps.accounts.views import user, client, traider

urlpatterns  = [
        # path('password/change/',
        #      auth_views.PasswordChangeView.as_view(),
        #      name='password_change'),
        path('password/change/',
                user.MyPasswordChangeView.as_view(),
                name='password_change'),
        path('password/change1/',
             user.MyPasswordChangeView1.as_view(),
             name='password_change'),
        path('password/change2/',
             user.MySettingsChangeView.as_view(),
             name='password_change'),
        path('password/change3/',
             user.MySettingsChangeView1.as_view(),
             name='password_change'),



# test url pu forma <-> view + 1

        path('password/change4/', user.MySettingsChangeView2.as_view(), name='password_change4'),
        path('password/change4/pass', user.MyPassChangeView2.as_view(), name='forma_password_change4'),
        path('password/change4/status', user.MyStatusChangeView2.as_view(), name='forma_status_change4'),

# END test url pu forma <-> view + 1



# path('password/change/done/',
#                 auth_views.PasswordChangeDoneView.as_view(),
#                 name='password_change_done'),
        path('password/change/done/',
                user.MyPasswordChangeDoneView.as_view(),
                name='password_change_done'),


#         path('password/reset/',
#                 auth_views.PasswordResetView.as_view(),
#                 name='password_reset'),
        path('password/reset/',
                user.MyPasswordResetView.as_view(),
                name='password_reset'),
        # path('password/reset/done/',
        #         auth_views.PasswordResetDoneView.as_view(),
        #         name='password_reset_done'),
        path('password/reset/done/',
                user.MyPasswordResetDoneView.as_view(),
                name='password_reset_done'),



        # re_path(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        #         auth_views.PasswordResetConfirmView.as_view(),
        #         name='password_reset_confirm'),
        re_path(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                user.MyPasswordResetConfirmView.as_view(),
                name='password_reset_confirm'),
        # path('password/reset/complete/',
        #         auth_views.PasswordResetCompleteView.as_view(),
        #         name='password_reset_complete'),
        path('password/reset/complete/',
                user.MyPasswordResetCompleteView.as_view(),
                name='password_reset_complete'),
]