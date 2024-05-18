"""
This document contains all the forms to handle the updates from the admin page
"""
from common.models.user import User
from django import forms


class UserForm(forms.ModelForm):
    """
    A form for updating user information in the admin page.

    Args:
        forms (ModelForm): A form for updating a User model instance.
    """
    class Meta:
        model = User
        fields = '__all__'
        exclude = ['profileImage']
