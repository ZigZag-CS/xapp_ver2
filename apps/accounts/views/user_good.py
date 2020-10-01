# -*- coding: utf-8 -*-


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
        context = self.get_context_data(**kwargs)
        # print(f" in POST context = {context['pass_form'].fields}")
        if request.POST.get('pass') is not None:
            print(f"************ pass > { request.POST.get('pass') } *********")
            password_form = MyPasswordChangeForm1(request.POST or None, user=request.user)
            if password_form.is_valid():
                print("Forma pass valida")
                messages.success(request, "Statutul parolei cu succes")
            else:
                print("Forma pass ne-valida")
                messages.error(request, "Forma pass ne-valida. Schimbatul parolei fara succes.")
                password_form = MyPasswordChangeForm1(user=request.user)

        elif request.POST.get('status') is not None:
            print(f"************ status > { request.POST.get('status') } *********")
            status_form = MyStatusChangeForm1(request.POST or None, user=request.user)
            if status_form.is_valid():
                print("Forma status valida")
                messages.success(request, "Statutul schimbat cu succes")
            else:
                print("Forma status ne-valida")
                messages.error(request, "Forma status ne-valida. Schimbatul statutului fara succes.")
                status_form = MyStatusChangeForm1(user=request.user)









        context = self.get_context_data()
        # # context['pass_form'] = password_form
        # # context['status_form'] = status_form
        return render(self.request, self.template_name, context)
