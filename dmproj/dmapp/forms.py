from django import forms
# from .models import UploadedFile

# class UploadFileForm(forms.ModelForm):
#     class Meta:
#         model = UploadedFile
#         fields = ['file']

class UploadFileForm(forms.Form):
    input1 = forms.FileField()
    input2 = forms.FileField()