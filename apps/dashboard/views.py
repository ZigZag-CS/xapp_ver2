from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, FormView, DetailView, View, UpdateView

#LoginRequiredMixin,
class AccountHomeView(LoginRequiredMixin, DetailView):

    template_name = 'dashboard/dashboard.html'

    def get_object(self):
        return self.request.user
