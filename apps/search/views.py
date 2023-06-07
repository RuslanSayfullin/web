from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import html
from django.views import generic

from apps.froze.models import Froze

User = get_user_model()


class SearchNewView(generic.TemplateView):
    raise_exception = True

    template_name = "search/search_new.html"

    def get_queryset(self, po_telefonu, po_adresu, po_imeni, po_nomery):
        if not po_telefonu and not po_adresu and not po_imeni and not po_nomery:
            return Froze.objects.none()

        client_qs = Froze.objects.all()
        if po_telefonu:
            po_telefonu = po_telefonu.strip()
            if str(po_telefonu)[:1] == '8' or str(po_telefonu)[:1] == '7':
                po_telefonu = po_telefonu[1:]
            client_qs = client_qs.filter(Q(phone__icontains=po_telefonu))
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
                client_qs = client_qs.filter(address__icontains=iskat_adres)
        if po_imeni:
            client_qs = client_qs.filter(name__icontains=po_imeni)
        if po_nomery:
            client_qs = client_qs.filter(nomer_dogovora__icontains=po_nomery)

        return client_qs.order_by("-id")[:50]

    def get_context_data(self, **kwargs):
        context = super(SearchNewView, self).get_context_data(**kwargs)

        po_telefonu = html.escape(self.request.GET.get("po_telefonu", ""))
        po_adresu = html.escape(self.request.GET.get("po_adresu", ""))
        po_imeni = html.escape(self.request.GET.get("po_imeni", ""))
        po_nomery = html.escape(self.request.GET.get("po_nomery", ""))

        context.update({
            'froze_items': self.get_queryset(po_telefonu, po_adresu, po_imeni, po_nomery),
        })
        return context


class SearchResultsView(SearchNewView):
    template_name = "search/search_results.html"