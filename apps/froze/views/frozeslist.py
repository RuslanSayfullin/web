from django.views import generic

from apps.froze.models import Froze


class FrozeLIstView(generic.ListView):
    template_name = 'froze/froze/frozes_all.html'
    context_object_name = "froze_items"
    paginate_by = 5


class FrozeAllView(FrozeLIstView):

    def get_queryset(self):
        return Froze.objects.all().order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super(FrozeAllView, self).get_context_data(**kwargs)
        return context
