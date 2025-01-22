from django import forms
from Chemist_Master.models import ChemistRegister
from  guide.models import guides

class ChemistRegisterform(forms.ModelForm):
    class Meta:
        model=ChemistRegister
        fields='__all__'

class guideForm(forms.ModelForm):
    class Meta:
        model = guides
        fields = "__all__"