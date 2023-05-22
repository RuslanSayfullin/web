from django.views import generic


class CreateUpdateDogovorIndi(generic.FormView):
    template_name = 'dogovora/create_update_indi.html'