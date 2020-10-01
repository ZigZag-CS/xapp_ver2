# -*- coding: utf-8 -*-
# from django.contrib.auth import get_user_model, authenticate, login
# from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import Http404, request
from django.utils.translation import gettext_lazy as _

# from django.urls import reverse
# from django.utils.decorators import method_decorator
# from django.http import HttpResponse
# from django.utils.safestring import mark_safe
from django.contrib.auth.views import *

from django.views.generic import CreateView, FormView, DetailView, View, UpdateView
from django.shortcuts import render, redirect, get_object_or_404

# from django.utils.http import is_safe_url

from django.views.generic.edit import FormMixin

from ..mixins import NextUrlMixin, RequestFormAttachMixin, ActivationRequiredMixin
from ..forms import *
from django.contrib.auth.forms import PasswordChangeForm
from ..models import *
from ..decorators import anonymous_required


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

@method_decorator(anonymous_required(redirect_url = '/'), name='dispatch')
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



@method_decorator(anonymous_required(redirect_url = '404error'), name='dispatch')
class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/'


class UserDetailUpdateView(LoginRequiredMixin ,UpdateView):
    form_class = UserDetailChangeForm
    # form_class = UserDetailChangeForm
    template_name = 'accounts/detail-update-view.html'
    # success_url = '/account/'

    # def get_object(self):
    #     return self.request.user
    #
    # def get_context_data(self, *args, **kwargs):
    #     context = super(UserDetailUpdateView, self).get_context_data(*args, **kwargs)
    #     context['title'] = 'Change Your account details'
    #     return context
    #
    # def get_success_url(self):
    #     return reverse("account:home")





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

class MyPasswordChangeView1(PasswordChangeView):
    # statuschange_form_class = StatusChangeForm1(self.request.GET or None)
    template_name = 'accounts/registration/password_change1.html'
    success_url = reverse_lazy('password_change_done')

    def dispatch(self, *args, **kwargs):
        print(f"===================")
        print("In functia dispatch()")
    #     print(f"request = {request}")
    #     print(f"request.user.user_status = {request.user.user_status}")
        print(f"*args = {args}")
        print(f"**kwargs {kwargs}")
        print(f"===================")
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        print(f"===================")
        print("In functia get_form_kwargs()")
        print(f"**kwargs {kwargs}")
        print(f"===================")
        return kwargs

    # def get(self, request, *args, **kwargs):
    #     print(f' functia get din MyPasswordChangeView1 ====== forma pu change pass {self.form_class} ======')
    #     # pass_form = self.form_class
    #     status_form = StatusChangeForm1(self.request.GET or None)
    #     context = self.get_context_data(**kwargs)
    #     context['status_form'] = status_form
    #     print(f'context = {context}')
    #     return render(request, self.template_name, {'status_form':status_form})
    #
    # def post(self, request, *args, **kwargs):
    #     print(f"===================")
    #     print("In functia post()")
    #     print(f"request = {request}")
    #     print(f"request.user.user_status = {request.user.user_status}")
    #     print(f"*args = {args}")
    #     print(f"**kwargs {kwargs}")
    #     print(f"===================")
    #     if 'status' in request.POST:
    #         print("======= STATUS =======")
    #
    #     if request.user.user_status == 0:
    #         return redirect('/dashboardc/home/')
    #     else:
    #         return redirect('/')
    #
    #     # return redirect('/dashboardc/home/')
    #     # return reverse("customer:customer-update")




class MySettingsChangeView(LoginRequiredMixin, TemplateView):
    # login_required = True
    # pass_form_class = MyPasswordChangeForm
    # status_form_class = MyStatusChangeForm
    template_name = 'accounts/registration/settings_pass_status_change.html'
    # model = User
    error_messages = {
        **SetPasswordForm.error_messages,
        'password_incorrect': _("Your old password was entered incorrectly. Please enter it again."),
    }



    def get(self, request, *args, **kwargs):
        print(f' functia get din MySettingsChangeView ====== forma pu change pass  ======')
    #     print(f' forma pu change pass {self.pass_form_class} ======')
    #     print(f' forma pu change status {self.status_form_class} ======')
    #     pass_form = self.pass_form_class
    #     status_form = self.status_form_class
    #     forms = {
    #         "pass_form": pass_form,
    #         'status_form': status_form
    #     }
    #     context = self.get_context_data(pass_form=pass_form, status_form=status_form)
    #     # context['pass_form'] = pass_form
    #     # context['status_form'] = status_form
    #     print(f'context = {context}')
    #     return self.render_to_response(context)
        context = self.get_context_data(**kwargs)
        print(f' functia get din MySettingsChangeView ====== {context}  ======')
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        extra_context = None
        context = super().get_context_data(**kwargs)
        context.update({
            'pass_form': MyPasswordChangeForm,
            'status_form': MyStatusChangeForm,
            **(self.extra_context or {})
        })
        print(f' functia get_context_data din MySettingsChangeView ====== {context}  ======')
        return context

    # @method_decorator(login_required)
    def post(self, request):
        post_data = request.POST or None
        print(f' functia post din MySettingsChangeView ====== {post_data}  ======')
        if 'pass' in self.request.POST:
            print(" srabotal pass")
            if self.request.POST['old_password'] and self.request.POST['new_password1'] and self.request.POST['new_password2']:
                if self.request.POST['new_password1'] == self.request.POST['new_password2']:
                    form_old_password = self.request.POST['old_password']
                    if not self.request.user.check_password(form_old_password):
                        print("parola veche incorecta")
                    else:
                        print(">>>>>>>>>>>>> PAROLA CORECTA <<<<<<<<<<<<")
                        self.request.user.set_password(self.request.POST['new_password1'])
                        self.request.user.save()
                else:
                    print("parolele nu coincid")
                    cont = "Password Error"
            else:
                cont = "Form Error"
            # cont = cont['old_password']
            # print(f' ==== in functia post === cont = {cont}')
        elif 'status' in self.request.POST:
            print(" srabotal status")
            if not request.user.is_active or not request.user.phone_active:
                return redirect('/')
            else:
                cont = self.request.POST
                # print(f"# ======= {cont['user_status']} ========= #")
                try:
                    new_status = cont['user_status']
                    print(f"# ======= {new_status} ========= #")
                except MultiValueDictKeyError:
                    new_status = request.user.user_status
                    print(f"# ======= {new_status} ========= #")
                curent_user = request.user.pk
                print(f"# ===curent_user==== {curent_user} ========= #")
                object = get_object_or_404(User, pk=curent_user)
                print(f"# ===object==== {object} ========= #")
                object.user_status = new_status
                object.save()
            # cont = int(self.request.POST.get('user_status', False))
            # print(f'======= {type(cont)} ======= {cont} =======')
            # new_status = int(cont['user_status'])
            # user_object = request.user.user_status
            # user_object = new_status
            # print(f' ==== in functia post === user_object = {user_object}')

            # if cont['user_status']:
            #     new_status = cont['user_status']
            # else:
            #     raise ValidationError(
            #         'Invalid value: %(value)s',
            #         code='invalid',
            #         params={'value': '42'},
            #     )

                print(f' ==== in functia post === cont = {cont}')
            # print(f' ==== in functia post === new_status = {new_status}')

        # print(f' ==== in functia post === request = {request}')

    #     pass_form = self.pass_form_class(post_data, prefix='pass')
    #     status_form = self.status_form_class(post_data, prefix='status')
    #
    #     context = self.get_context_data(pass_form=pass_form,
    #                                     status_form=status_form)
    #
    #     if pass_form.is_valid():
    #         self.form_save(pass_form)
    #     if status_form.is_valid():
    #         self.form_save(status_form)
    #
    #     return self.render_to_response(context)
        return redirect('/dashboardc/home/')

    # def form_save(self, form):
    #     obj = form.save()
    #     messages.success(self.request, "{} saved successfully".format(obj))
    #     return obj
    #
    # def get(self, request, *args, **kwargs):
    #     return self.post(request, *args, **kwargs)

class MySettingsChangeView1(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/registration/settings_pass_status_change.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'pass_form': MyPasswordChangeForm1(user=self.request.user),
            'status_form': MyStatusChangeForm1(user=self.request.user)
        })
        print(f' MySettingsChangeView1 functia get_context_data => {context}  ======')
        return context

    def get(self, request, *args, **kwargs):
        # print(f' MySettingsChangeView1 functia get  ====== > ======')
        context = self.get_context_data(**kwargs)
        # context['pass_form'] = MyPasswordChangeForm1(user=self.request.user)
        # context['status_form'] = MyStatusChangeForm1(user=self.request.user)
        # print(f' MySettingsChangeView1 functia get => {context}  ======')
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print(f' ##### MySettingsChangeView1 functia POST  ======  ======')
        # context = self.get_context_data(**kwargs)
        # print(f" in POST context = {context['pass_form'].fields}")
        # if request.POST.get('pass') is not None:
        #     print(f"************ pass > { request.POST.get('pass') } *********")
        #     password_form = MyPasswordChangeForm1(request.POST or None, user=request.user)
        #     if password_form.is_valid():
        #         print("Forma pass valida")
        #         messages.success(request, "Statutul parolei cu succes")
        #     else:
        #         print("Forma pass ne-valida")
        #         messages.error(request, "Forma pass ne-valida. Schimbatul parolei fara succes.")
        #         password_form = MyPasswordChangeForm1(user=request.user)
        #
        # elif request.POST.get('status') is not None:
        #     print(f"************ status > { request.POST.get('status') } *********")
        #     status_form = MyStatusChangeForm1(request.POST or None, user=request.user)
        #     if status_form.is_valid():
        #         print("Forma status valida")
        #         messages.success(request, "Statutul schimbat cu succes")
        #     else:
        #         print("Forma status ne-valida")
        #         messages.error(request, "Forma status ne-valida. Schimbatul statutului fara succes.")
        #         status_form = MyStatusChangeForm1(user=request.user)


        # if request.method == 'POST':
        #     password_form = MyPasswordChangeForm1(request.POST or None, user=request.user)
        #     # print("Schimbam parola")
        #     if password_form.is_valid():
        #         print("Forma pass valida")
        #         messages.success(request, "Statutul parolei cu succes")
        #     else:
        #         print("Forma pass ne-valida")
        #         messages.error(request, "Forma pass ne-valida. Schimbatul parolei fara succes.")
        # else:
        #     password_form = MyPasswordChangeForm1(user=request.user)
        #
        #
        # if request.method == 'POST' and not password_form.is_valid():
        #     status_form = MyStatusChangeForm1(request.POST or None, user=request.user)
        #     password_form = MyPasswordChangeForm1(user=request.user)
        #     # print("Schimbam statutul")
        #     if status_form.is_valid():
        #         print("Forma status valida")
        #         messages.success(request, "Statutul schimbat cu succes")
        #     else:
        #         print("Forma status ne-valida")
        #         messages.error(request, "Forma status ne-valida. Schimbatul statutului fara succes.")
        # else:
        #     status_form = MyStatusChangeForm1(user=request.user)

        # print(f' ##### MySettingsChangeView1 functia POST >> context = self.get_context_data(**kwargs) => {context["pass_form"]}  ======')
        # print(f' ##### MySettingsChangeView1 functia POST >> context = self.get_context_data(**kwargs) => {context["status_form"]}  ======')
        # print(f" Metoda PUT forma password_form == {password_form}")
        # print(f" Metoda PUT forma status_form == {status_form}")

        if 'pass' in self.request.POST:
            password_form = MyPasswordChangeForm1(request.POST or None, user=request.user)
            if password_form.is_valid():
                print("Schimbam parola")
                self.request.user.set_password(password_form.data['new_password1'])
                self.request.user.save()
                update_session_auth_hash(request, password_form.user)
                return redirect('/')
            else:
                context = self.get_context_data(**kwargs)
                context['pass_form'] = password_form
                # context['status_form'] = MyStatusChangeForm1(user=request.user)
                return render(self.request, self.template_name, context)

        if 'status' in self.request.POST:
            status_form = MyStatusChangeForm1(request.POST or None, user=request.user)
            if status_form and status_form.is_valid():
                print("Schimbam statutul")
                if not request.user.is_active or not request.user.phone_active:
                    return redirect('/')
                else:
                    cont = self.request.POST
                    try:
                        new_status = cont['user_status']
                        # print(f"# ======= {new_status} ========= #")
                    except MultiValueDictKeyError:
                        new_status = request.user.user_status
                        # print(f"# ======= {new_status} ========= #")
                    curent_user = request.user.pk
                    # print(f"# ===curent_user==== {curent_user} ========= #")
                    object = get_object_or_404(User, pk=curent_user)
                    # print(f"# ===object==== {object} ========= #")
                    object.user_status = new_status
                    object.save()
                return redirect('/')
            else:
                context = self.get_context_data(**kwargs)
                context['status_form'] = status_form
                # context['pass_form'] = MyPasswordChangeForm1(user=request.user)
                return render(self.request, self.template_name, context)



        # print(f"++++++++++++++ put == password_form.data = {password_form.data['new_password1']} ++++++++++++++")
        # print(f"********** put == password_form.cleaned_data = {password_form.data['status']} ****************")
        # print(f"********** put == password_form.cleaned_data.get = {password_form.cleaned_data.get('new_password1')} ****************")
        # print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        # status_form = MyStatusChangeForm1(user=request.user, data=request.POST or None)
        # print(f"********** put == statuss_form.cleaned_data = {status_form.data} ****************")
        # print(f"pana la validare, forma password_form.cleaned_data = {password_form.cleaned_data}")
        # if 'pass' in self.request.POST:
        #     print("Schimbam parola")
        #     password_form = MyPasswordChangeForm1(user=request.user, data=request.POST or None)
        #     if password_form.is_valid():
        #         print("forma validaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        #         # print(f"forma password_form.cleaned_data = {password_form.cleaned_data}")
        #         self.request.user.set_password(password_form.data['new_password1'])
        #         self.request.user.save()
        #         update_session_auth_hash(request, password_form.user)
        #         return redirect('/')
        #     else:
        #         print("password_form NE validaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        # elif 'status' in self.request.POST:
        #     print("Schimbam statutul")
        #     status_form = MyStatusChangeForm1(user=request.user, data=request.POST or None)
        #     if status_form.is_valid():
        #         return redirect('/')
        #     else:
        #         print("status_form NE validaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        #
        # else:
        #     print("forma NE validaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")


        context = self.get_context_data()
        # # context['pass_form'] = password_form
        # # context['status_form'] = status_form
        return render(self.request, self.template_name, context)

        # return redirect('/accounts/password/change3/')
        # form = self.get_form()
        # post_data = request.POST or None
        # form_pas = post_data.get('pass_form')
        # print(f"********** put == form = {form_pas}")
        # if 'pass' in self.request.POST:
        #     print(" srabotal pass3")
        #     form_pas = self.request.POST.get('pass_form')
        #     print(f"********** put == form_pass = {form_pas} ****************")
        #     if self.request.POST['old_password'] and self.request.POST['new_password1'] and self.request.POST['new_password2']:
        #         if self.request.POST['new_password1'] == self.request.POST['new_password2']:
        #             form_old_password = self.request.POST['old_password']
        #             if not self.request.user.check_password(form_old_password):
        #                 print("staryi paroli nepravel'nyj")
        #             else:
        #                 print(">>>>>>>>>>>>> Pass iz correct <<<<<<<<<<<<")
        #                 self.request.user.set_password(self.request.POST['new_password1'])
        #                 self.request.user.save()
        #         else:
        #             print("paroli ne sovpadaet")
        #             cont = "Password Error"
        #     else:
        #         cont = "Form Error"
        # elif 'status' in self.request.POST:
        #     print(" srabotal status3")
        #     if not request.user.is_active or not request.user.phone_active:
        #         return redirect('/')
        #     else:
        #         cont = self.request.POST
        #         try:
        #             new_status = cont['user_status']
        #             print(f"# ======= {new_status} ========= #")
        #         except MultiValueDictKeyError:
        #             new_status = request.user.user_status
        #             print(f"# ======= {new_status} ========= #")
        #         curent_user = request.user.pk
        #         print(f"# ===curent_user==== {curent_user} ========= #")
        #         object = get_object_or_404(User, pk=curent_user)
        #         print(f"# ===object==== {object} ========= #")
        #         object.user_status = new_status
        #         object.save()

# test alta versiune bazata pe fiecare forma cu view-ul sau *****

class MySettingsChangeView2(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/registration/settings_pass_status_change1.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'pass_form': MyPasswordChangeForm2(user=self.request.user),
            'status_form': MyStatusChangeForm2(user=self.request.user)
        })
        print(f' MySettingsChangeView2 functia get_context_data => {context}  ======')
        return context

class MyPassChangeView2(MySettingsChangeView2):
    template_name = 'accounts/registration/settings_pass_status_change1.html'

    def get(self, *args, **kwargs):
        return redirect(reverse("password_change4"))

    def post(self, request, *args, **kwargs):
        password_form = MyPasswordChangeForm1(request.POST or None, user=request.user)
        if password_form.is_valid():
            print("Forma pass valida")
            self.request.user.set_password(password_form.data['new_password1'])
            self.request.user.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, "Statutul parolei cu succes")
        else:
            print("Forma pass ne-valida")
            messages.error(request, "Forma pass ne-valida. Schimbatul parolei fara succes.")
            password_form = MyPasswordChangeForm1(user=request.user)

        context = self.get_context_data()
        context.update({'pass_form': password_form})
        return render(self.request, self.template_name, context)

class MyStatusChangeView2(MySettingsChangeView2):
    template_name = 'accounts/registration/settings_pass_status_change1.html'

    def get(self, *args, **kwargs):
        return redirect(reverse("password_change4"))

    def post(self, request, *args, **kwargs):
        status_form = MyStatusChangeForm1(request.POST or None, user=request.user)
        if not request.user.is_active or not request.user.phone_active:
            messages.error(request, "Schimbatul statutului imposibila, trebuie de cativat numarul de telefon.")
            status_form = MyStatusChangeForm1(user=request.user)
        else:
            if status_form.is_valid():
                print("Forma status valida")
                new_status = status_form.cleaned_data['user_status']
                print(new_status)
                curent_user = request.user.pk
                object = get_object_or_404(User, pk=curent_user)
                object.user_status = new_status
                object.save()
                messages.success(request, "Statutul schimbat cu succes")
            else:
                print("Forma status ne-valida")
                messages.error(request, "Forma status ne-valida. Schimbatul statutului fara succes.")
                status_form = MyStatusChangeForm1(user=request.user)

        context = self.get_context_data()
        context.update({'status_form': status_form})
        return render(self.request, self.template_name, context)


# END test alta versiune bazata pe fiecare forma cu view-ul sau *****

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