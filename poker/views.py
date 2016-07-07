# coding: utf-8

from django.views.generic.edit import FormView
from poker.forms import PokerHandDataForm


class TaskOneView(FormView):
    template_name = 'task_one.html'
    form_class = PokerHandDataForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        parse_result = form.parse_result()
        context = self.get_context_data(parse_result=parse_result)
        return self.render_to_response(context)
