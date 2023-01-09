from django import forms
from newsportal.models import Category


class CatForm(forms.Form):
    form = forms.MultipleChoiceField(choices=Category.objects.all().values_list('name', flat=True))
