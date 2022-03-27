import re

from django import forms

from system.models import Profile


def email_check(email):
    pattern = re.compile(r"\"?([-a-zA-Z0-9.'?{}]+@\w+\.\w+)\"?")
    return re.match(pattern, email)


class RegistrationForm(forms.Form):
    username = forms.CharField(label='username', max_length=50, help_text="username")
    email = forms.EmailField(label='email', help_text="email")
    password = forms.CharField(label='password', help_text="password", widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')

        filter_result = Profile.objects.filter(username__exact=username)
        if len(filter_result) > 0:
            raise forms.ValidationError('该用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email_check(email):
            filter_result = Profile.objects.filter(email__exact=email)
            if len(filter_result) > 0:
                raise forms.ValidationError("this email is aleary exist!")
        else:
            raise forms.ValidationError("please input format email!")

        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')

        return password


class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=50, help_text="username or email")
    password = forms.CharField(label='password', widget=forms.PasswordInput, help_text="password")

    # print(username, password)
    # use clean methods to define custom validation rules

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if email_check(username):
            filter_result = Profile.objects.filter(email__exact=username)
            if not filter_result:
                raise forms.ValidationError('该账号不存在')
        else:
            filter_result = Profile.objects.filter(username__exact=username)
            if not filter_result:
                raise forms.ValidationError('该账号不存在')

        return username
