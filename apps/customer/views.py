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

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        print(f'get:context = {context}')
        return self.render_to_response(context)

    def get_object(self):
        print(f'get_object(self): {self.request.user}')
        return self.request.user