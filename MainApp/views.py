from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.models import Snippet
from MainApp.forms import SnippetForm


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    if request.method == "GET":
        form = SnippetForm()
        context = {'pagename': 'Добавление нового сниппета',
                   'form': form }
        return render(request, 'pages/add_snippet.html', context)
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("snippets_list")
        return render(request,'pages/add_snippet.html',{'form': form})


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





def snippet_delete(request, snippet_id):
    context = {'pagename': 'Удаление сниппета'}
    try:
        snippet = Snippet.objects.get(id=snippet_id)
        context = context | {'snippet': snippet}
    except:
        return render(request, 'pages/error.html', context | {'error': f'not found {snippet_id}'},)

    if request.method == "POST":

        snippet = Snippet.objects.get(id=snippet_id)

        snippet.delete()
        return redirect("snippets_list")
    return render(request, 'pages/del_snippet.html', context)


def snippet_edit(request, snippet_id):
    context = {'pagename': 'Редактирование сниппета'}
    try:
        snippet = Snippet.objects.get(id=snippet_id)
        context = context | {'snippet': snippet}
    except:
        return render(request, 'pages/error.html', context | {'error': f'not found {snippet_id}'},)
    if request.method == "GET":
        form = SnippetForm(instance=snippet)
        context = context = context | {'form': form }
        return render(request, 'pages/edit_snippet.html', context)
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("snippets_list")
        return render(request,'pages/edit_snippet.html',{'form': form})
