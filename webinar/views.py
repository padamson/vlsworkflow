from django.http.response import HttpResponse
from django.http import HttpResponse

# Create your views here.
def home_page(request):
    return HttpResponse('<html><title>Webinar To-Do Lists</title></html>')