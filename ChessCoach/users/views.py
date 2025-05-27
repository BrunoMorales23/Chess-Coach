from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def register_page(request):
    register = request.GET.get("register")
    print(register)
    #Register devuelve como STR
    if request.method == "GET" and register == "true":
        #Register View
        return render(request, 'logInPanel.html', {'register': True})
    
    elif request.method == "GET" and register == None:
        logout(request)
        return redirect('landing') 

    elif request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()  # si es un ModelForm (modelos personalizados no funcionan con save!)
            username = form.cleaned_data.get('username')

            #DJANGO soporta variables de sesión
            request.session['username'] = username
            request.session['logged_in'] = True
            return redirect("landing")
        else:
            request.session['status'] = "invalidcreds"
            return render(request, "logInPanel.html", {"error": "Invalid credentials", 'register': True})
    else:
        #Log In View
        form = RegisterForm()
        return render(request, 'logInPanel.html', {'register': False})
    

def login_page(request):
    status = request.session.get('status', None)
    if request.method == "GET" and status == "invalidcreds":
        return render(request, 'logInPanel.html', {'register': False})
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)  # crea la sesión
            request.session['username'] = username
            request.session['logged_in'] = True
            return redirect("landing")
        else:
            return render(request, "logInPanel.html", {"error": "Invalid credentials", 'register': False})

    return render(request, "logInPanel.html")
