# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from apps.accounts.models import User


class CustomerDetailUpdateForm(ModelForm):

    class Meta:
        model = User
        fields = ['email', 'full_name', 'avatar', 'country', 'city', 'address', 'phone_number']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'})
            # 'avatar': forms.ClearableFileInput(attrs={'multiple': False})
            # 'country': CountrySelectWidget()
        }

    # full_name = forms.CharField()

    # class Meta:
    #     model = User
    #     # fields = '__all__'
    #     fields = ['email', 'full_name', 'country', 'city', 'address', 'phone_number' ]
    #     # fields = ['full_name', 'avatar', 'country', 'city', 'address', 'phone_number' ]
    #     # widgets = {'country': CountrySelectWidget()}


class CustomerDetailUpdateForm1(ModelForm):

   class Meta:
        model = User
        fields = ['email', 'full_name', 'avatar', 'country', 'city', 'address', 'phone_number' ]
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'})
            # 'avatar': forms.ClearableFileInput(attrs={'multiple': False})
            # 'country': CountrySelectWidget()
        }
