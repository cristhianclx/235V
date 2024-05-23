from django.forms import ModelForm
from web.models import Search


class SearchForm(ModelForm):
    class Meta:
        model = Search
        fields = ("day_name", "enterprise", "month_name", "date_to_search", "type_flight",)