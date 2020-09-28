# -*- coding: utf-8 -*-

# Users.py

class MySettingsChangeView1(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/registration/settings_pass_status_change.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'pass_form': None,
            'status_form': None
        })
        # print(f' MySettingsChangeView1 functia get_context_data => {context}  ======')
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['pass_form'] = MyPasswordChangeForm1(user=self.request.user)
        context['status_form'] = MyStatusChangeForm1(user=self.request.user)
        # print(f' MySettingsChangeView1 functia get => {context}  ======')
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print(f' MySettingsChangeView1 functia post  ======  ======')
        # password_form = MyPasswordChangeForm1(user=request.user, data=request.POST or None)
        # print(f"++++++++++++++ put == password_form.data = {password_form.data['new_password1']} ++++++++++++++")
        # print(f"********** put == password_form.cleaned_data = {password_form.data['status']} ****************")
        # print(f"********** put == password_form.cleaned_data.get = {password_form.cleaned_data.get('new_password1')} ****************")
        # print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        # status_form = MyStatusChangeForm1(user=request.user, data=request.POST or None)
        # print(f"********** put == statuss_form.cleaned_data = {status_form.data} ****************")
        # print(f"pana la validare, forma password_form.cleaned_data = {password_form.cleaned_data}")
        if 'pass' in self.request.POST:
            print("Schimbam parola")
            password_form = MyPasswordChangeForm1(user=request.user, data=request.POST or None)
            if password_form.is_valid():
                print("forma validaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                # print(f"forma password_form.cleaned_data = {password_form.cleaned_data}")
                self.request.user.set_password(password_form.data['new_password1'])
                self.request.user.save()
                update_session_auth_hash(request, password_form.user)
                return redirect('/')
            else:
                print("password_form NE validaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        elif 'status' in self.request.POST:
            print("Schimbam statutul")
            status_form = MyStatusChangeForm1(user=request.user, data=request.POST or None)
            if status_form.is_valid():
                return redirect('/')
            else:
                print("status_form NE validaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        #
        # else:
        #     print("forma NE validaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

        context = self.get_context_data()
        # context['pass_form'] = password_form
        # context['status_form'] = status_form
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


# forms.py

class MyPasswordChangeForm1(forms.Form):
    ''' forma de modificarea parolei utilizatorului '''

    old_password = forms.CharField(strip=False, widget=forms.PasswordInput())
    new_password1 = forms.CharField(strip=False, widget=forms.PasswordInput())
    new_password2 = forms.CharField(strip=False, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        print(f"MyPasswordChangeForm1 metoda __init__ a clasei formei parolei, self.user = {self.user}")
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        print(f"In MyPasswordChangeForm1 functia clean_old_password()")
        cleaned_data = super().clean()
        print(f"In MyPasswordChangeForm1 functia clean_old_password(), cleaned_data = {cleaned_data}")
        if cleaned_data:
            print(f"cleaned_data['old_password'] => {cleaned_data['old_password']}")
            if self.user and not self.user.check_password(cleaned_data['old_password']):
                self.add_error('old_password', 'Current password is not valid')
        return cleaned_data

    def clean(self):
        print(f"In MyPasswordChangeForm1 functia clean()")
        cleaned_data = super().clean()
        print(f"In MyPasswordChangeForm1 functia clean(), cleaned_data = {cleaned_data}")
        if cleaned_data:
            if ('new_password1' in cleaned_data) and ('new_password2' in cleaned_data):
                if cleaned_data['new_password1'] != cleaned_data['new_password2']:
                    self.add_error('new_password2', 'New password confirmation is not same to new password')
            else:
                print("nu-s valori pu parole")
                # self.add_error('new_password1', 'New password must be')
                raise ValidationError("Please enter data", code='invalid')
        else:
            raise ValidationError("Please enter data", code='invalid')
        # print(f"in clean() din forma self.user = {self.user}")
        # if self.user and not self.user.check_password(cleaned_data['old_password']):
        #     self.add_error('old_password', 'Current password is not valid')
        # print(f"**** add_error din clean() din MyPasswordChangeForm1 => {self.add_error}")
        return cleaned_data

    def is_valid(self):
        print(f"In MyPasswordChangeForm1 functia is_valid()")
        return self.is_bound and not self.errors


class MyStatusChangeForm1(forms.Form):
    ''' forma de schimbare a statutului utilizatorului '''

    user_status = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        print(f"MyStatusChangeForm1 metoda __init__ a clasei formei statutului, self.user = {self.user}")
        super().__init__(*args, **kwargs)

    def clean(self):
        print(f"In MyStatusChangeForm1 functia clean()")
        cleaned_data = super().clean()
        print(f" ----- cleaned_data => {cleaned_data}")
        if cleaned_data:
        # if cleaned_data['user_status']:
            print(f"cleaned_data => {cleaned_data['user_status']}")
        else:
            self.add_error('user_status', 'need check status')
        return cleaned_data

    def is_valid(self):
        print(f"In MyStatusChangeForm1 functia is_valid()")
        return self.is_bound and not self.errors
