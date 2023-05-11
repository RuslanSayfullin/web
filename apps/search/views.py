from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.utils import html
from django.views import generic

from apps.froze.models import Froze

User = get_user_model()


class SearchNewView(PermissionRequiredMixin, generic.TemplateView):
    raise_exception = True
    template_name = "search/search_new.html"
    permission_required = ''

    def get_queryset(self, po_telefonu, po_adresu, po_imeni):
        if not po_telefonu and not po_adresu and not po_imeni:
            return Froze.objects.none()

        froze_qs = Froze.objects.all()
        if po_telefonu:
            po_telefonu = po_telefonu.strip()
            if str(po_telefonu)[:1] == '8' or str(po_telefonu)[:1] == '7':
                po_telefonu = po_telefonu[1:]
            froze_qs = froze_qs.filter(Q(phone__icontains=po_telefonu) | Q(phone_two__icontains=po_telefonu))
        if po_adresu:
            po_adresu = po_adresu.replace(',', ' ').replace('/', ' ')
            po_adresu = po_adresu.split(' ')
            adres = []
            digits = '0123456789'
            for one in po_adresu:
                if len(one) >= 5:
                    adres.append(one)
                    continue
                one_new = []
                for d in one:
                    if d in digits:
                        one_new.append(d)
                one_new = ''.join(one_new)
                if len(one_new) >= 1:
                    adres.append(one_new)
            for iskat_adres in adres:
                froze_qs = froze_qs.filter(address__icontains=iskat_adres)
        if po_imeni:
            froze_qs = froze_qs.filter(name__icontains=po_imeni)


        return froze_qs.order_by("-id")[:50]

    def get_context_data(self, **kwargs):
        context = super(SearchNewView, self).get_context_data(**kwargs)

        po_telefonu = html.escape(self.request.GET.get("po_telefonu", ""))
        po_adresu = html.escape(self.request.GET.get("po_adresu", ""))
        po_imeni = html.escape(self.request.GET.get("po_imeni", ""))

        context.update({
            'client_items': self.get_queryset(po_telefonu, po_adresu, po_imeni),
        })
        return context


class SearchResultsView(SearchNewView):
    template_name = "search/search_results.html"