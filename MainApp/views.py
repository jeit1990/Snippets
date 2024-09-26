from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.models import Snippet

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    context = {'pagename': 'Добавление нового сниппета'}
    return render(request, 'pages/add_snippet.html', context)


def snippets_page(request):
    snippets = Snippet.objects.all()
    context = {'pagename': 'Просмотр сниппетов', 'snippets': snippets}
    return render(request, 'pages/view_snippets.html', context)


def get_snippet(request, snippet_id):
    context = {'pagename': 'Просмотр сниппета'}
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except:
        return render(request, 'pages/error.html', context | {'error': f'not found {snippet_id}'},)
    else:
        context = context | {'snippet': snippet}
        return render(request, 'pages/snippet.html', context)