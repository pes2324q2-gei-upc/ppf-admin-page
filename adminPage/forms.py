"""
This document contains all the forms to handle the updates from the admin page
"""
from common.models.user import User
from django import forms


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
