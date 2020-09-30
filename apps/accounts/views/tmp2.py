
# views.py

class MySettingsChangeView1(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/registration/settings_pass_status_change.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'pass_form': None,
            'status_form': None
        })
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['pass_form'] = MyPasswordChangeForm1(user=self.request.user)
        context['status_form'] = MyStatusChangeForm1(user=self.request.user)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if 'pass' in self.request.POST:
            password_form = MyPasswordChangeForm1(request.POST or None, user=request.user)
            if password_form.is_valid():
                print("Password change")
                self.request.user.set_password(password_form.data['new_password1'])
                self.request.user.save()
                update_session_auth_hash(request, password_form.user)
                return redirect('/')
            else:
                context = self.get_context_data(**kwargs)
                context['pass_form'] = password_form
                context['status_form'] = MyStatusChangeForm1(user=request.user)
                return render(self.request, self.template_name, context)

        if 'status' in self.request.POST:
            status_form = MyStatusChangeForm1(request.POST or None, user=request.user)
            if status_form and status_form.is_valid():
                print("Status change")
                if not request.user.is_active or not request.user.phone_active:
                    return redirect('/')
                else:
                    cont = self.request.POST
                    try:
                        new_status = cont['user_status']
                    except MultiValueDictKeyError:
                        new_status = request.user.user_status
                    curent_user = request.user.pk
                    object = get_object_or_404(User, pk=curent_user)
                    object.user_status = new_status
                    object.save()
                return redirect('/')
            else:
                context = self.get_context_data(**kwargs)
                context['status_form'] = status_form
                context['pass_form'] = MyPasswordChangeForm1(user=request.user)
                return render(self.request, self.template_name, context)

        context = self.get_context_data()
        return render(self.request, self.template_name, context)


# forms.py

class MyPasswordChangeForm1(forms.Form):

    old_password = forms.CharField(strip=False, widget=forms.PasswordInput())
    new_password1 = forms.CharField(strip=False, widget=forms.PasswordInput())
    new_password2 = forms.CharField(strip=False, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        cleaned_data = super().clean()
        if cleaned_data:
            if self.user and not self.user.check_password(cleaned_data['old_password']):
                self.add_error('old_password', 'Current password is not valid')
        return cleaned_data

    def clean(self):
        cleaned_data = super().clean()
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
        return cleaned_data

    def is_valid(self):
        return self.is_bound and not self.errors


class MyStatusChangeForm1(forms.Form):

    user_status = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data:
            if not ('user_status' in cleaned_data):
                self.add_error('user_status', 'need check status')
        else:
            raise ValidationError("Please enter data", code='invalid')

        return cleaned_data

    def is_valid(self):
        return self.is_bound and not self.errors
