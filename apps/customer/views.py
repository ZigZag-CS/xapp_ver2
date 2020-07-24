from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import ModelFormMixin

from .decorators import *
from apps.accounts.models import User
from django.views.generic import CreateView, FormView, DetailView, View, UpdateView

#LoginRequiredMixin,
from .forms import CustomerDetailUpdateForm


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

@method_decorator(customer_required, name='dispatch')
class CustomerDetailUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomerDetailUpdateForm
    template_name = 'customer/customer-profile.html'

    # success_url = '/account/'

    def get_object(self):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super(CustomerDetailUpdateView, self).get_context_data(*args, **kwargs)
        # context['title'] = 'Change Your account details'
        # print(f"CustomerDetailUpdateView => get_context_data => context[form] = {context['form']} ")
        return context

    def get_success_url(self):
        return reverse("customer:dashboard-home")

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(ModelFormMixin, self).get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        print(f'kwargs = {kwargs}')
        return kwargs

    # def form_valid(self, form):
    #     # Сохраняем данные полученные из POST
    #     # self.object = form.save(commit = False)
    #     instance = form.save()
    #     print(f'CustomerDetailUpdateView =>form_valid=> intsance = {instance}')
    #     instance.save()
    #     return super(CustomerDetailUpdateView, self).form_valid(form)