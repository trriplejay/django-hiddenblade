from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout


class HomepageView(TemplateView):
    template_name = "index.html"


class ThanksView(TemplateView):
    template_name = "thanks.html"

"""
class LoginView(TemplateView):
    template_name = "login.html"
#    username = request.POST['username']
#    password = request.POST['password']
#    user = authenticate(username=username, password=password)
"""

class LogoutView(TemplateView):
    template_name = "logout.html"
