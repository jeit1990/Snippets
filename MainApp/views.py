from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from MainApp.models import Snippet
from MainApp.forms import SnippetForm, UserRegistrationForm
from django.contrib import auth
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)

@login_required
def add_snippet_page(request):
    if request.method == "GET":
        form = SnippetForm()

        context = {'pagename': 'Добавление нового сниппета',
                   'form': form }
        return render(request, 'pages/add_snippet.html', context)
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            n_snip = form.save(commit=False)
            if request.user.is_authenticated:
                n_snip.user = request.user
                n_snip.save()
            return redirect("snippets_list")
        return render(request,'pages/add_snippet.html',{'form': form})


@login_required
def snippets_page_user(request, user_name):
    snippets = Snippet.objects.filter(user__username=user_name)
    context = {'pagename': 'Просмотр сниппетов', 'snippets': snippets}
    return render(request, 'pages/view_snippets.html', context)


def snippets_page(request):
    snippets = Snippet.objects.filter(public_snippet=True)
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


def snippet_delete_my(request, snippet_id):
    context = {'pagename': 'Удаление сниппета'}
    try:
        snippet = Snippet.objects.get(id=snippet_id)
        context = context | {'snippet': snippet}
    except:
        return render(request, 'pages/error.html', context | {'error': f'not found {snippet_id}'},)

    if request.method == "POST":
        snippet.delete()
        return redirect("snippets_list")
    return render(request, 'pages/del_snippet.html', context)


@login_required
def snippet_edit(request, snippet_id):

    context = {'pagename': 'Редактирование сниппета'}
    try:
        snippet = Snippet.objects.get(id=snippet_id)
        if request.user != snippet.user:
            return render(request, 'pages/error.html', context | {'error': f'Нельзя редактировать чужие сниппеты'},)
        context = context | {'snippet': snippet}
    except:
        return render(request, 'pages/error.html', context | {'error': f'not found {snippet_id}'},)
    if request.method == "GET":
        form = SnippetForm(instance=snippet)
        context = context | {'form': form }
        return render(request, 'pages/edit_snippet.html', context)
    if request.method == "POST":
        """snippet.name = request.POST['name']
        snippet.code = request.POST['code']
        snippet.lang = request.POST['lang']"""
        data = request.POST
        for key, value in data.items():
            setattr(snippet, key, value)
        """print(request.POST)
        print(hasattr(request.POST, "public_snippet"))"""
        """try:
            data["public_snippet"]
            snippet.public_snippet = True
        except:
            snippet.public_snippet = False"""
        if data.get("public_snippet") is None:
            snippet.public_snippet = False
        else:
            snippet.public_snippet = True
        snippet.save()
        return redirect("snippets_list")
        #return render(request,'pages/edit_snippet.html',{'form': form})


@login_required
def snippet_delete(request, snippet_id):
    if request.method == "GET" or request.method == "POST":
        snippet = get_object_or_404(Snippet, id=snippet_id)
        if request.user != snippet.user:
            return render(request, 'pages/error.html', context | {'error': f'Нельзя редактировать чужие сниппеты'},)
        snippet.delete()
        return redirect("snippets_list")
    #return render(request, 'pages/del_snippet.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            # Return error message
            context = {
                'pagename': 'PythonBin',
                "errors": "wrong username or password"
            }
            return render(request, "pages/index.html", context)
    return redirect('home')


def logout(request):
    auth.logout(request)
    return  redirect('home')


def create_user(request):
    context = {"pagename": "Регистрация"}
    if request.method == "GET":
        form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context["form"] = form
    return render(request, 'pages/registration.html', context)