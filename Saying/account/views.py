from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from .models import Account


@csrf_exempt
def start(request):
    if request.method == "POST":
        good = request.POST['username']
        data = serializers.serialize("json", Account.objects.all())
        return HttpResponse(data, content_type='application/json')
    return HttpResponse("no data")
