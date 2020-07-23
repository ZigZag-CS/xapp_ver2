# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django_countries.widgets import CountrySelectWidget

from apps.accounts.models import User


class CustomerDetailUpdateForm(ModelForm):
    # full_name = forms.CharField()


    class Meta:
        model = User
        # fields = '__all__'
        fields = ['full_name', 'country', 'city', 'address', 'phone_number' ]
        # fields = ['full_name', 'avatar', 'country', 'city', 'address', 'phone_number' ]
        # widgets = {'country': CountrySelectWidget()}
