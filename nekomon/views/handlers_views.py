"""
Client and server errors handlers
"""

from django.shortcuts import render
from django.utils.translation import gettext_lazy as _


def handler404(request, exception):
    """Error 404 handler"""
    
    context = {
        "message": _("This page does not exist.")
    }

    return render(request, "handlers.html", context)


def handler500(request):
    """Error 500 handler"""
    
    context = {
        "message": _("An error has occurred. Please, contact Rufino to help you solve it.")
    }

    return render(request, "handlers.html", context)
