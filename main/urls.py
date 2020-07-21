"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth.views import LogoutView

from .views import eroare_404

from apps.accounts.views import user, client, traider

urlpatterns = [
    path('admin/', admin.site.urls),
    path('404error/', eroare_404, name="404error"),

    path("", include("apps.pages.urls", namespace='pages')),

    # path('accounts/login/', RedirectView.as_view(url='/login')),
    path('accounts/', RedirectView.as_view(url='/account')),
    path('account/', include("apps.accounts.urls", namespace='account')),
    path('accounts/', include("apps.accounts.passwords.urls")),

    path('register/', user.RegisterView.as_view(), name="register"),
    path('login/', user.LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),

    path('dashboardc/', include("apps.customer.urls", namespace='customer')),
    path('dashboards/', include("apps.traider.urls", namespace='traider')),

    path('settings/', RedirectView.as_view(url='/account')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_title = "EU ... treshi la kuru meu"
admin.site.site_header = "EU ... treshi la kuru meu"
