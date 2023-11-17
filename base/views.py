from django.shortcuts import render


TITLE = "icodely"
TITLE_WITH_DOT = " • " + TITLE


def index_page(request):
    """Render a main page"""
    return render(request, "base/index.html", {"title": TITLE})
