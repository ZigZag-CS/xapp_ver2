# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django_countries.widgets import CountrySelectWidget

from apps.accounts.models import User


class CustomerDetailUpdateForm(ModelForm):
    # full_name = forms.CharField()

    def form_valid(self, form):
        # Сохраняем данные полученные из POST
        # self.object = form.save(commit = False)
        instance = form.save()
        print(f'CustomerDetailUpdateView =>form_valid=> intsance = {instance}')
        instance.save()
        return super(CustomerDetailUpdateForm, self).form_valid(form)

    class Meta:
        model = User
        # fields = '__all__'
        fields = ['full_name', 'country', 'city', 'address', 'phone_number' ]
        # fields = ['full_name', 'avatar', 'country', 'city', 'address', 'phone_number' ]
        # widgets = {'country': CountrySelectWidget()}
