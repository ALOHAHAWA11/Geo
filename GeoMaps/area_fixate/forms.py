from django import forms

from area_fixate.validators import check_cadastral


class GetMapAreaForm(forms.Form):
    cadastral_number = forms.CharField(max_length=255, label='Кадастровый номер',
                                       widget=forms.TextInput(attrs={'placeholder': 'Введите номер',}),
                                       validators=[check_cadastral])
