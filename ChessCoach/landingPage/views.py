from django.shortcuts import render, redirect
from django.contrib.auth import logout

# Create your views here.

def landing_page(request):
    logged_in = request.session.get('logged_in', False)
    if request.method == "GET" and logged_in != False:
        logout_validation = request.GET.get("logout")
        print(logout)
        if logout_validation == 'true':
            logout(request)
            return redirect('landing')
        else:
            username = request.session.get('username', False)
            return render(request, 'landingPage.html', {'logged' : logged_in, 'username': username})
    else:
        return render(request, 'landingPage.html')

def logout_view(request):
    logout(request)
    return redirect('landing_page')
