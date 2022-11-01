from django import forms
from django.forms import ModelForm

from .models import MyUser

# https://www.youtube.com/watch?v=quJzUzCs6Q0
# https://stackoverflow.com/questions/9324432/how-to-create-password-input-field-in-django


class myForm(forms.ModelForm):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={"placeholder": "email",
                                       "class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "password",
                                          "class": "form-control"}))

    class Meta:
        model = MyUser
        fields = ('email', 'password')


class newPasswordForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={"placeholder": "email",
                                       "class": "form-control"}))
