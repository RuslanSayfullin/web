from django.views import generic

from apps.dogovora import forms


class CreateUpdateDogovorIndi(generic.FormView):
    template_name = 'dogovora/create_update_indi.html'
    form_class = forms.DogovorIndiForm
