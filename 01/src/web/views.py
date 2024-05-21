from django.shortcuts import render
from web.models import Person


def personsView(request):
    items = Person.objects.all()
    return render(request, 'persons/list.html', {
        "items": items,
    })