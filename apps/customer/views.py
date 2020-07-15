from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from .decorators import *
from apps.accounts.models import User
from django.views.generic import CreateView, FormView, DetailView, View, UpdateView

#LoginRequiredMixin,
@method_decorator(customer_required, name='dispatch')
class AccountHomeView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'customer/dashboard.html'

    def get_object(self):
        return self.request.user