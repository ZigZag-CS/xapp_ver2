# -*- coding: utf-8 -*-
from django import forms

from apps.accounts.models import User


class CustomerDetailChangeForm(forms.ModelForm):
    full_name = forms.CharField(
        label="Name",
        required=False,
        widget = forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ['full_name']