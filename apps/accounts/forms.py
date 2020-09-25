# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField, PasswordChangeForm
from django.utils.safestring import mark_safe
from django.utils.translation import gettext, gettext_lazy as _

from .models import *

User = get_user_model()



class ReactivateEmailForm(forms.Form):
    email       = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = EmailActivation.objects.email_exists(email)
        if not qs.exists():
            register_link = reverse("register")
            msg = """This email does not exists, would you like to <a href="{link}">register</a>?
            """.format(link=register_link)
            raise forms.ValidationError(mark_safe(msg))
        return email



class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('full_name', 'email', ) #'full_name',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserDetailChangeForm(forms.ModelForm):
    full_name = forms.CharField(
        label="Name",
        required=False,
        widget = forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ['full_name', 'user_status']




class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    # password = ReadOnlyPasswordHashField()

    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "user's password, but you can change the password using "
            "<a href=\"../password/\">this form</a>."
        ),
    )

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password', 'is_active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]



class GuestForm(forms.Form):
    # email    = forms.EmailField()
    class Meta:
        model = GuestEmail
        fields = [
            'email'
        ]

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(GuestForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        # Save the provided password in hashed format
        obj = super(GuestForm, self).save(commit=False)
        if commit:
            obj.save()
            request = self.request
            request.session['guest_email_id'] = obj.id
        return obj


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        request = self.request
        data = self.cleaned_data
        email = data.get("email")
        password = data.get("password")
        qs = User.objects.filter(email=email)
        print(f'qs == {qs}')
        if qs.exists():
            # user email is registered, check active/
            not_active = qs.filter(is_active=False)
            if not_active.exists():
                ## not active, check email activation
                link = reverse("account:resend-activation")
                reconfirm_msg = """Go to <a href='{resend_link}'>
                        resend confirmation email</a>.
                        """.format(resend_link=link)
                confirm_email = EmailActivation.objects.filter(email=email)
                is_confirmable = confirm_email.confirmable().exists()
                print(f'is_confirmable == {is_confirmable}')
                if is_confirmable:
                    msg1 = "Please check your email to confirm your account or " + reconfirm_msg.lower()
                    print(f'mark_safe(msg1) == {mark_safe(msg1)}')
                    raise forms.ValidationError(mark_safe(msg1))
                email_confirm_exists = EmailActivation.objects.email_exists(email).exists()
                if email_confirm_exists:
                    msg2 = "Email not confirmed. " + reconfirm_msg
                    raise forms.ValidationError(mark_safe(msg2))
                if not is_confirmable and not email_confirm_exists:
                    raise forms.ValidationError("This user is inactive.")
        user = authenticate(request, username=email, password=password)
        if user is None:
            raise forms.ValidationError("Data iz invalid, suka")
        login(request, user)
        self.user = user
        return data

    # def form_valid(self, form):
    #     request = self.request
    #     next_ = request.GET.get('next')
    #     next_post = request.POST.get('next')
    #     redirect_path = next_ or next_post or None
    #     email  = form.cleaned_data.get("email")
    #     password  = form.cleaned_data.get("password")

    #     print(user)
    #     if user is not None:
    #         if not user.is_active:
    #             print('inactive user..')
    #             messages.success(request, "This user is inactive")
    #             return super(LoginView, self).form_invalid(form)
    #         login(request, user)
    #         user_logged_in.send(user.__class__, instance=user, request=request)
    #         try:
    #             del request.session['guest_email_id']
    #         except:
    #             pass
    #         if is_safe_url(redirect_path, request.get_host()):
    #             return redirect(redirect_path)
    #         else:
    #             return redirect("/")
    #     return super(LoginView, self).form_invalid(form)


# seamana oleaka cu UserAdminCreationForm
class RegisterForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm pass", widget=forms.PasswordInput)
    agree = forms.BooleanField(label="Confirm agreement", widget=forms.CheckboxInput)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        # print(self.cleaned_data)
        user.set_password(self.cleaned_data["password"])
        # user.is_active = False  # send confirmation email
        user.is_active = True  # send confirmation email
        if commit:
            user.save()
        return user


    class Meta:
        model = User
        fields = ('full_name', 'email', )  # 'full_name',)


# class StatusChangeForm(forms.Form):
class StatusChangeForm(forms.ModelForm):
    # fild1 = forms.BooleanField(label="Customer")
    # fild2 = forms.BooleanField(label="Traider")

    class Meta:
        model = User
        fields = ('user_status',)
        # widgets = {
        #     'user_status': forms.BooleanField
        # }

class StatusChangeForm1(forms.Form):
    fild1 = forms.BooleanField(label="Customer")
    fild2 = forms.BooleanField(label="Traider")

    def clean(self):
        print(f"In functia clean(), data = {self.data}")


class MyPasswordChangeForm(PasswordChangeForm):
    ''' forma de modificarea parolei utilizatorului '''

    # def is_valid(self):
    #     print(f"In function is_valid() from MyPasswordChangeForm")
    #     return self.errors

    # def clean_old_password(self):
    #     """
    #     Validate that the old_password field is correct.
    #     """
    #     print(f" >>>> in clean_old_password din MyPasswordChangeForm <<<<")
    #     old_password = self.cleaned_data["old_password"]
    #     if not self.user.check_password(old_password):
    #         raise forms.ValidationError(
    #             self.error_messages['password_incorrect'],
    #             code='password_incorrect',
    #         )
    #     return old_password

class MyStatusChangeForm(forms.Form):
    ''' forma de schimbare a statutului utilizatorului '''

    # def __init__(self, request, *args, **kwargs):
    #     self.request = request
    #     super(MyStatusChangeForm, self).__init__(*args, **kwargs)
    #
    # def clean(self):
    #     cleaned_data = super().clean()
    #     print(f"In functia clean(), data = {self.data}")
    #     request = self.request
    #     # data = self.cleaned_data
    #     return cleaned_data
    #
    # def is_valid(self):
    #     print(f"In functia is_valid(), data = ")
    #     return self.is_bound and not self.errors

    # def clean_recipients(self):
    #     data = super(MyStatusChangeForm, self).clean()
    #     print(f"In functia clean_recipients(), data = {data}")
    #     return data

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
