from django.forms import ModelForm
from web.models import Person


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ('name', 'age', 'description')