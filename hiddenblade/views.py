from django.views.generic import TemplateView

class HomepageView(TemplateView):
    template_name = "index.html"
class ThanksView(TemplateView):
    template_name = "thanks.html"