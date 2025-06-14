from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login

def register_page(request):
    register = request.GET.get("register")
    #Register devuelve como STR
    if request.method == "GET":
        #Register View, pero sin excepcionar, renderizado
        return render(request, 'logInPanel.html', {'register': True, 'usersView' : True})

    elif request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # si es un ModelForm (modelos personalizados no funcionan con save!)
            request.session['status'] = None
            username = form.cleaned_data.get('username')

            #DJANGO soporta variables de sesión
            request.session['username'] = username
            request.session['logged_in'] = True
            return redirect("landing")
        else:
            return render(request, 'logInPanel.html', { 'register': True, 'usersView': True, 'form': form})
    else:
        #Log In View
        form = RegisterForm()
        return render(request, 'logInPanel.html', {'register': False, 'usersView' : True})
    

def login_page(request):
    status = request.session.get('status', None)
    if request.method == "GET" and status == "invalidcreds":
        return render(request, 'logInPanel.html', {'register': False, 'usersView' : True})
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # crea la sesión
            request.session['username'] = username
            request.session['logged_in'] = True
            return redirect("landing")
        else:
            return render(request, "logInPanel.html", {"error": "Invalid credentials", 'register': False, 'usersView' : True})

    return render(request, "logInPanel.html", {'register': False, 'usersView' : True})

def profile_page(request, username):
    if request.method == "GET":
        username = request.session.get('username')
        return render(request, 'profile.html', {'username': username})