from django.shortcuts import render, redirect
from django.views.generic import View
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from web.utils import normalize, parseFile, job_vectorizer, job_matrix, ranker
from web.forms import DocumentForm
from web.models import Document, DocumentMatch


class IndexView(View):

    def get(self, request):
        form = DocumentForm()
        return render(request, "index.html", {"form": form})
    
    def post(self, request):
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            document_in_text = parseFile(instance.cv)
            text_to_match = normalize(document_in_text)
            cv_serie = pd.Series(text_to_match)
            cv_matrix = job_vectorizer.transform(cv_serie)
            ranking = cosine_similarity(cv_matrix, job_matrix, True)
            ranking_serie = pd.Series(ranking[0])
            ranker['RANKING'] = ranking_serie
            ranker_final = ranker.sort_values('RANKING', ascending=False)
            for r in ranker_final.index:
                if ranker_final["RANKING"][r]>=0.1:
                    DocumentMatch.objects.create(
                        document=instance,
                        position=ranker_final["PUESTO"][r],
                        url=ranker_final["URL"][r],
                        ranking=ranker_final["RANKING"][r],
                    )
            return redirect('results', id=instance.id)
        else:
            return redirect('index')
        

class ResultsView(View):

    def get(self, request, id):
        instance = Document.objects.get(id = id)
        matches = DocumentMatch.objects.filter(document = instance,).all().order_by("-ranking")
        return render(request, "results.html", {"matches": matches})