from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from MainApp.forms import SnippetForm, UserRegistrationForm
from MainApp.models import Snippet
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def my_snippets(request):
    snippets = Snippet.objects.filter(user=request.user)  
    context = {
        'pagename': 'Мои сниппеты',
        'snippets': snippets
        }
    return render(request, 'pages/view_snippets.html', context)


@login_required(login_url='home')
def add_snippet_page(request):
    # Создаем пустую форму при запросе GET
    if request.method == "GET":
        form = SnippetForm()
        context = {
            'pagename': 'Добавление нового сниппета',
            'form': form
            }
        return render(request, 'pages/add_snippet.html', context)
    
    # Получаем данные из формы и на их основе создаем новый Сниппет в БД
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            if request.user.is_authenticated:
                snippet.user = request.user
                snippet.save()
            return redirect("snippets-list")  # GET /snippets/list
        return render(request,'pages/add_snippet.html', {'form': form})


def snippets_page(request):
    snippets = Snippet.objects.filter(mode='public')  
    #snippets = Snippet.objects.all()
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets
        }
    return render(request, 'pages/view_snippets.html', context)


def snippet_detail(request, snippet_id):
    context = {'pagename': 'Просмотр сниппета'}
    try:
        snippet = Snippet.objects.get(pk=snippet_id)
    except Snippet.DoesNotExist:
        return render(request, "pages/errors.html", context | {"error": f"Snippet with id={snippet_id} not found."})
    else:
        context["snippet"] = snippet
        context["type"] = "view"
        return render(request, "pages/snippet_detail.html", context)

@login_required
def snippet_edit(request, snippet_id):
    context = {'pagename': 'Редактирование сниппета'} 
    try:
        snippet = Snippet.objects.get(pk=snippet_id)
    except ObjectDoesNotExist:
        raise Http404
    if snippet.user_id == request.user.id:
    # Variant 1 с помощью SnippetForm
    # if request.method == "GET":
    #     form = SnippetForm(instance=snippet)
    #     return render(request,"pages/add_snippet.html", {"form": form})

    # Variant 2
    # Хотим получить страницу с данными сниппета
        if request.method == "GET":
            context = {
                "snippet": snippet,
                "type": "edit"
            }
            return render(request, "pages/snippet_detail.html", context)

    # Получаем данные из формы и на их основе меняем значения Сниппета
        if request.method == "POST":
            data_form = request.POST
            snippet.name = data_form["name"]
            snippet.code = data_form["code"]
            snippet.save()
            return redirect("snippets-list")
    else:
        return redirect("snippets-list")

@login_required
def snippet_delete(request, snippet_id):
    if request.method == "GET" or request.method == "POST":
        snippet = get_object_or_404(Snippet, id=snippet_id)
        if snippet.user_id == request.user.id:
            snippet.delete()
            return redirect('snippets-list')
        else:
            return redirect("snippets-list")

def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        # print("username =", username)
        # print("password =", password)
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            context = {
                'pagename': "PythonBin",
                "errors": ['wrong username or password'],
            }
            return render(request, "pages/index.html", context)
    return redirect('home')


def logout(request):
    auth.logout(request)
    return redirect("home")

def my_snippets_page(request):
    form_user = request.user.id
    snippets = Snippet.objects.filter(user_id=form_user)      
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets
        }
    return render(request, 'pages/view_snippets.html', context)

def create_user(request):
    context = {"pagename":"Регистрация нового пользователя"}
    # Создаем новую форму при запросе методом GET
    if request.method == "GET":
        form = UserRegistrationForm()
    
    # Получаем данные из формы и на их основе создаем нового пользователя в БД
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")

    context["form"] = form
    return render(request, "pages/registration.html", context)