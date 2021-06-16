from django import forms
from view_animals.models import Animal


class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = '__all__'
