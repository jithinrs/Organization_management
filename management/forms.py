from typing import Any
from django import forms
from .models import MyUser


class SignupForm(forms.ModelForm):
    password = forms.CharField()
    confirm_password = forms.CharField()
    class Meta:
        model = MyUser
        fields = ['email', 'password', 'confirm_password']
    

    def clean(self):
        print('checkpoint1')
        cleaned_data = super(SignupForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Password does not match")
