from django.shortcuts import render

# Create your views here.

def landing_page(request):
    logged_in = request.session.get('logged_in', False)
    if request.method == "GET" and logged_in != False:
        username = request.session.get('username', False)
        return render(request, 'landingPage.html', {'logged' : logged_in, 'username': username})
    else:
        return render(request, 'landingPage.html')
