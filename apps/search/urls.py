from django.urls import path, re_path

from apps.search.views import SearchNewView, SearchResultsView

app_name = "search"
urlpatterns = [
    re_path(r'^new$', SearchNewView.as_view(), name="search_new"),
    re_path(r'^search_results$', SearchResultsView.as_view(), name="search_results"),
]