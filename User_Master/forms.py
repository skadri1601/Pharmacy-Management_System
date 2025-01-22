from django import forms
from User_Master.models import UserRegister,UserQuery

class UserRegisterForm(forms.ModelForm):
    class Meta:
        model=UserRegister
        fields='__all__'

class UserQueryForm(forms.ModelForm):
    class Meta:
        model=UserQuery
        fields='__all__'
    