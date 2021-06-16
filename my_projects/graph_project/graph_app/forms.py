from django.forms import ModelForm

from .models import Vector, Graph


class VectorForm(ModelForm):
    class Meta:
        model = Vector
        fields = '__all__'


class GraphForm(ModelForm):
    class Meta:
        model = Graph
        fields = '__all__'
