from django.http import HttpResponse

def index(request):
    return HttpResponse("Olá mundo, você está no index das eleições.")

# Create your views here.
