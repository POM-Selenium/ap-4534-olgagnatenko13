from django import forms


class AuthorForm(forms.Form):
    name = forms.CharField(max_length=20)
    surname = forms.CharField(max_length=20)
    patronymic = forms.CharField(max_length=20, required=False)