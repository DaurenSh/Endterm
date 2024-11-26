import logging
from django.shortcuts import render
from django.views import View

logger = logging.getLogger(__name__)

class RegisterPageView(View):
    def get(self, request):
        logger.info("Register page accessed")
        return render(request, 'users/register.html')


class LoginPageView(View):
    def get(self, request):
        logger.info("Login page accessed")
        return render(request, 'users/login.html')
