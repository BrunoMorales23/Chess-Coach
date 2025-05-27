from django.shortcuts import render, redirect
from django.contrib.auth import logout
#from django.contrib.auth.decorators import login_required

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
        
    elif request.method == "POST":
        username = request.session.get('username', False)
        return render(request, 'landingPage.html', {'error' : 'Bad Used or Credentials, please, try again'})

    else:
        return render(request, 'landingPage.html')

#@login_required(login_url='login')
#def test_feature(request):
#    return render(request, "landingPage.html")