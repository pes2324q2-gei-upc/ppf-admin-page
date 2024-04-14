from django.http import HttpResponse
from django.shortcuts import render
from common.models.user import Driver, User 

# Create your views here.
def home(request):
    users = User.objects.all()
    return render(request, "views/users.html", {"users": users})