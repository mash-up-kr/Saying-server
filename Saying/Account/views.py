from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from .models import UserProfile
from django.core import serializers
User = get_user_model()


@csrf_exempt
@require_POST
def register_user(request):
    # get data from post
    user_acc = request.POST.get('acc')
    password = request.POST.get('pwd')
    nickname = request.POST.get('nm')
    age = request.POST.get('age')
    gender = request.POST.get('gender')

    if not all([user_acc, password, nickname, age, gender]):
        return HttpResponseBadRequest("No key or null value in POST params")
    else:
        print("register user")
        # user = User.objects.create_user(user_acc=user_acc, password=password)
        # user.userprofile.nickname = nickname
        # user.userprofile.age = age
        # user.userprofile.gender = gender
        # user.save()
        return HttpResponse("success")


@csrf_exempt
def update_profile(request):
    if request.method == "POST":
        user = UserProfile.objects.get(userid=request.POST['userid'])
        user.nickname = request.POST['nickname']
        user.save()
        # data = serializers.serialize("json", User.objects.all())
        # return HttpResponse(data, content_type='application/json')
        return HttpResponse("success")
    return HttpResponse("no data")
