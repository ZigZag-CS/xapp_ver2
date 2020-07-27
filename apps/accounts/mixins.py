# -*- coding: utf-8 -*-
from django.utils.http import is_safe_url


class RequestFormAttachMixin(object):

    def get_form_kwargs(self):
        # print("RequestFormAttachMixin:get_form_kwargs")
        kwargs = super(RequestFormAttachMixin, self).get_form_kwargs()
        kwargs['request'] = self.request
        # print(f"RequestFormAttachMixin:get_form_kwargs - kwargs: {kwargs}")
        return kwargs


class NextUrlMixin(object):
    default_next = "/"

    def get_next_url(self):
        print("NextUrlMixin:get_next_url")
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        # print(f'>>>>> redirect_path = {redirect_path}')
        if is_safe_url(redirect_path, request.get_host()):
                return redirect_path
        return self.default_next