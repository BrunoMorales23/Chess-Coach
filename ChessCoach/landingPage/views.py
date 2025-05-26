from django.shortcuts import render

# Create your views here.

def landing_page(request):
    if request.method == "GET":
        return render(request, 'landingPage.html')

