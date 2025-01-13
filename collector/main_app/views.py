from django.shortcuts import render
from django.http import HttpResponse


# Define the home view
def home(request):
    return render(request, 'home.html')

def about(request):
    # return HttpResponse("<h1>About the cat collector</h1>")
    return render(request, 'about.html')

def car_index(request):
    return render(request, 'cars/index.html' , {'cars': cars})