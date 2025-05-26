from django.shortcuts import render, redirect
from .forms import RegisterForm

def register_page(request):
    register = request.GET.get("register")
    #Register devuelve como STR
    if request.method == "GET" and register == "true":
        #Register View
        return render(request, 'logInPanel.html', {'register': True})
    
    elif request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()  # si es un ModelForm (modelos personalizados no funcionan con save!)
            username = form.cleaned_data.get('username')

            #DJANGO soporta variables de sesión
            request.session['username'] = username
            request.session['logged_in'] = True
        return redirect('landing')
    
    else:
        #Log In View
        form = RegisterForm()
        return render(request, 'logInPanel.html', {'register': False})
    

def login_page(request):
    if request.method == "GET":
        return render(request, 'landingPage.html')
