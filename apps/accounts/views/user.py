# -*- coding: utf-8 -*-
# from django.contrib.auth import get_user_model, authenticate, login
# from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.http import Http404
from django.utils.translation import gettext_lazy as _

# from django.urls import reverse
# from django.utils.decorators import method_decorator
# from django.http import HttpResponse
# from django.utils.safestring import mark_safe
from django.contrib.auth.views import *

from django.views.generic import CreateView, FormView, DetailView, View, UpdateView
from django.shortcuts import render, redirect

# from django.utils.http import is_safe_url

from django.views.generic.edit import FormMixin

from ..mixins import NextUrlMixin, RequestFormAttachMixin
from ..forms import *
from ..models import *



User = get_user_model()


# @login_required # /accounts/login/?next=/some/path/
# def account_home_view(request):
#     return render(request, "accounts/home.html", {})


#LoginRequiredMixin,
class AccountHomeView(LoginRequiredMixin, DetailView):

    template_name = 'accounts/home.html'
    # template_name = './acc'

    def get_object(self):
        return self.request.user


class AccountEmailActivateView(FormMixin, View):
    success_url = '/login/'
    form_class = ReactivateEmailForm
    key = None

    def get(self, request, key=None, *args, **kwargs):
        self.key = key
        # print(f'KEY >>>>>>>>>>>> {key} <<<<<<<<<<<<<<<')
        if key is not None:
            qs = EmailActivation.objects.filter(key__iexact=key)
            # print(f'AccountEmailActivateView => get: {qs.EmailActivation}')
            confirm_qs = qs.confirmable()
            if confirm_qs.count() == 1:
                obj = confirm_qs.first()
                obj.activate()
                messages.success(request, "Your email has been confirmed. Please login.")
                return redirect("login")
            else:
                activated_qs = qs.filter(activated=True)
                if activated_qs.exists():
                    reset_link = reverse("password_reset")
                    msg = """Your email has already been confirmed
                            Do you need to <a href="{link}">reset your password</a>?
                            """.format(link=reset_link)
                    messages.success(request, mark_safe(msg))
                    return redirect("login")
        context = {
            'form': self.get_form(),
            'key': key
        }
        return render(request, 'accounts/registration/activation-error.html', context)

    def post(self, request, *args, **kwargs):
        # create form to receive an email
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        msg = """Activation link sent, please check your email."""
        request = self.request
        messages.success(request, msg)
        email = form.cleaned_data.get("email")
        obj = EmailActivation.objects.email_exists(email).first()
        user = obj.user
        new_activation = EmailActivation.objects.create(user=user, email=email)
        new_activation.send_activation()
        return super(AccountEmailActivateView, self).form_valid(form)

    def form_invalid(self, form):
        context = {'form': form, "key": self.key}
        return render(self.request, 'registration/activation-error.html', context)

class GuestRegisterView(NextUrlMixin, RequestFormAttachMixin, CreateView):
    form_class = GuestForm
    default_next = '/register/'

    def get_success_url(self):
        return self.get_next_url()

    def form_invalid(self, form):
        return redirect(self.default_next)

# def guest_register_view(request):
#     form = GuestForm(request.POST or None)
#     context = {
#         "form": form
#     }
#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirect_path = next_ or next_post or None
#     if form.is_valid():
#         email       = form.cleaned_data.get("email")
#         new_guest_email = GuestEmail.objects.create(email=email)
#         request.session['guest_email_id'] = new_guest_email.id
#         if is_safe_url(redirect_path, request.get_host()):
#             return redirect(redirect_path)
#         else:
#             return redirect("/register/")
#     return redirect("/register/")


class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'accounts/login.html'
    default_next = '/'

    def form_valid(self, form):
        print("form valid in LoginView")
        next_path = self.get_next_url()
        print(f'LoginView : def form_valid - next_path: {next_path}')
        return redirect(next_path)


class RegisterView(UserPassesTestMixin, CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/'
    error_url = '/404error/'

    def test_func(self):
        error_path = '/register'
        user = str(self.request.user)
        request = self.request.user
        good_user = "AnonymousUser"
        # print(f'RegisterView => test_func {type(user)}')
        if user != good_user:
            print(f"RegisterView => test_func in IF {self.request.user}")
            # raise Http404("No MyModel matches the given query.")
            # return redirect(self.error_url)
            return render(request, '404.html', {})
        else:
            # print("inainte de reverse")
            # return reverse('/register')
            # return redirect(error_path)
            return redirect(error_path)

        #     print(f'RegisterView = {self.request.user}')




class UserDetailUpdateView(LoginRequiredMixin ,UpdateView):
    form_class = UserDetailChangeForm
    template_name = 'accounts/detail-update-view.html'
    # success_url = '/account/'

    def get_object(self):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Change Your account details'
        return context

    def get_success_url(self):
        return reverse("account:home")





# def login_page(request):
#     form = LoginForm(request.POST or None)
#     context = {
#         "form": form
#     }
#     # print(request.user.is_authenticated)
#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirect_path = next_ or next_post or None
#     if form.is_valid():
#         # print(form.changed_data)
#         username = form.cleaned_data.get("username")
#         password = form.cleaned_data.get("password")
#         user = authenticate(request, username=username, password=password)
#         # print(user)
#         # print(request.user.is_authenticated)
#         if user is not None:
#             # print(request.user.is_authenticated)
#             login(request, user)
#             try:
#                 del request.session['guest_email_id']
#             except:
#                 pass
#             if is_safe_url(redirect_path, request.get_host()):
#                 return redirect(redirect_path)
#             else:
#                 return redirect("/")
#         else:
#             # Return daca login e invalid, mesaj de eroare
#             print("Error")
#     return render(request, "accounts/login.html", context)
#
#
# def register_page(request):
#     form = RegisterForm(request.POST or None)
#     context = {
#         "form": form
#     }
#     if form.is_valid():
#         # print(form.changed_data)
#         # username = form.cleaned_data.get("username")
#         # email = form.cleaned_data.get("email")
#         # password = form.cleaned_data.get("password")
#         # new_user = User.objects.create_user(username, email, password)
#         # print(f'new user: {new_user}')
#         form.save()
#     return render(request, "accounts/register1.html", context)
#


class MyPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/registration/password_change.html'
    success_url = reverse_lazy('password_change_done')

class MyPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'accounts/registration/password_change_done.html'
    title = _('Password change successful')

class MyPasswordResetView(PasswordResetView):
    template_name = 'accounts/registration/forgot-password.html'

class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/registration/password_reset_done.html'
    title = _('Password reset sent')

class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/registration/password_reset_confirm.html'
    title = _('Enter new password please')

class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/registration/password_reset_complete.html'
    title = _('Malaghetz, Password reset complete')