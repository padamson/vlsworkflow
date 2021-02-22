from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from webinar.models import Item

def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/webinars/the-only-webinar-list')
    return render(request, 'home.html')

def view_list(request):
    items = Item.objects.all()
    return render(request, 'webinar.html', {'items': items})