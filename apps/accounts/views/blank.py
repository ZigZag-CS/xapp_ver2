# -*- coding: utf-8 -*-
from django.shortcuts import redirect, get_object_or_404, render
from django.utils.datastructures import MultiValueDictKeyError

from apps.accounts.forms import MyPasswordChangeForm, MyStatusChangeForm


class MySettingsChangeView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/registration/settings_pass_status_change.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        extra_context = None
        context = super().get_context_data(**kwargs)
        context.update({
            'pass_form': MyPasswordChangeForm,
            'status_form': MyStatusChangeForm,
            **(self.extra_context or {})
        })
        return context

    def post(self, request):
        post_data = request.POST or None
        if 'pass' in self.request.POST:
            print(" srabotal pass")
            if self.request.POST['old_password'] and self.request.POST['new_password1'] and self.request.POST['new_password2']:
                if self.request.POST['new_password1'] == self.request.POST['new_password2']:
                    form_old_password = self.request.POST['old_password']
                    if not self.request.user.check_password(form_old_password):
                        print("staryi paroli nepravel'nyj")
                    else:
                        print(">>>>>>>>>>>>> Pass iz correct <<<<<<<<<<<<")
                        self.request.user.set_password(self.request.POST['new_password1'])
                        self.request.user.save()
                else:
                    print("paroli ne sovpadaet")
                    cont = "Password Error"
            else:
                cont = "Form Error"
        elif 'status' in self.request.POST:
            print(" srabotal status")
            if not request.user.is_active or not request.user.phone_active:
                return redirect('/')
            else:
                cont = self.request.POST
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
        return redirect('/dashboardc/home/')



class MyStatusChangeForm(forms.Form):
    pass

class MyPasswordChangeForm(PasswordChangeForm):
    pass

