from django import forms
from web.models import Document

class DocumentForm(forms.ModelForm):
    cv = forms.FileField(
        label="Subir CV",
        widget=forms.FileInput(
            attrs={"class": "form-control form-control-lg"}
        )
    )
    
    class Meta:
        model = Document
        fields = ("cv",)