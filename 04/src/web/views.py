from django.shortcuts import render
from django.views.generic import View

from web.forms import DocumentForm


class IndexView(View):

    def get(self, request):
        form = DocumentForm()
        return render(request, "index.html", {"form": form})