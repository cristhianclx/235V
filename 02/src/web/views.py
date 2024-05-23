from django.shortcuts import render, redirect
from web.forms import SearchForm
from web.models import Search
from web.utils import normalize
from web.ml import predict

import pandas as pd


def homeView(request):
    if request.method == "GET":
        form = SearchForm()
        return render(request, "home.html", {"form": form})
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            item = form.save()
            data = pd.DataFrame({
                "TIPOVUELO": item.type_flight,
                "Fecha-I": item.date_to_search.strftime("%Y-%m-%d %H:%M:%S"), # 2017-01-01 23:30:00
                "MES": item.month_name,
                "OPERA": item.enterprise,
                "DIANOM": item.day_name,
            }, index=[0])
            features = normalize(data)
            result = predict(features)
            prediction = result[0]
            item.prediction = prediction
            item.save()
            return redirect("/predictions/{}".format(item.id))
        else:
            return render(request, "home.html", {"form": form})
        

def predictionView(request, id):
    item = Search.objects.get(id = id)
    return render(request, "predictions.html", {"item": item})