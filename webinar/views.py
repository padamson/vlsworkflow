from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from webinar.models import Item

#TODO: separate lists for each webinar
#TODO: autogenerate webinar to-do lists
#TODO: clean up after FT runs
def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')

    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})