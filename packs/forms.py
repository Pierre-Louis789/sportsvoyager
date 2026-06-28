

from django import forms
from .models import Pack


class PackForm(forms.ModelForm):
    class Meta:
        model = Pack
        fields = [
            'title',
            'club',
            'league',
            'price',
            'description',
            'is_premium',
            'image_name',
        ]
