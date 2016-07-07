# coding: utf-8
import json

from django.core.urlresolvers import reverse

from django.http import JsonResponse
from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.views.decorators.csrf import csrf_exempt
from poker.forms import PokerHandDataForm
from poker.detect import PokerHandAnalyzer


class TaskOneView(FormView):
    template_name = 'task_one.html'
    form_class = PokerHandDataForm

    def get_context_data(self, **ctx):
        ctx = super(TaskOneView, self).get_context_data(**ctx)
        ctx["task_two_url"] = self.request.build_absolute_uri(reverse('task_two'))
        return ctx

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        parse_result = form.parse_result()
        context = self.get_context_data(parse_result=parse_result)
        return self.render_to_response(context)


@csrf_exempt
def task_two(request):
    res = {}
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except ValueError:
            res["result"] = "JSON Parse Error"
            return JsonResponse(res)
        if "cards" not in data:
            res["result"] = "Cards List Required!!"
            return JsonResponse(res)

        lang_code = data.get("lang_code", "jp")
        pa = PokerHandAnalyzer(lang_code=lang_code)
        result = []
        counter = 0
        best_score = 100
        best_card_index = 0
        for card in data.get("cards"):
            parse_data = {}
            parse_data["card"] = card
            if pa.parse(card) is False:
                parse_data["parse_error"] = pa.parse_error_msg
            else:
                parse_data["hand"] = pa.get_hand_type()
            sort_index = pa.get_hand_sort_order()
            if(best_score < pa.get_hand_sort_order()):
                best_score = sort_index
                best_card_index = counter
            result.append(parse_data)
            counter += 1
        result[best_card_index]["best"] = True
        res["result"] = result
        return JsonResponse(res)

    else:
        # url = request.get_full_path()
        url = request.build_absolute_uri(request.META.get("PATH_INFO"))
        help_text = 'curl -X POST %s -d \'{"cards": ["H1 H13 H12 H11 H10", "H9 C9 S9 H2 C2"]}\'' % url
        return HttpResponse(help_text, content_type="text/plain; charset=us-ascii")
