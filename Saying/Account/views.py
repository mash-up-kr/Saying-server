from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from .models import UserProfile
from .tokens import account_activation_token
from .s3 import get_s3_object
from django.core import serializers
from django.template.loader import render_to_string
from django.core.mail import send_mail

User = get_user_model()


@csrf_exempt
def acc_check(request):
    if request.method == "POST":
        user_acc = request.POST.get('acc')

        if User.objects.filter(user_acc=user_acc).exists():
            return HttpResponse("already exists user")
        else:
            return HttpResponse("OK")
    return HttpResponseBadRequest("required POST method")


@csrf_exempt
def register_user(request):
    if request.method == "POST":
        user_acc = request.POST.get('acc')
        password = request.POST.get('pwd')
        nickname = request.POST.get('nm')
        age = request.POST.get('age')
        gender = request.POST.get('gender')

        if not all([user_acc, password, nickname, age, gender]):
            return HttpResponseBadRequest("No key or null value in POST params")
        else:
            user = User.objects.create_user(user_acc=user_acc, password=password)
            user.userprofile.nickname = nickname
            user.userprofile.age = age
            user.userprofile.gender = gender
            user.save()

            subject = 'Activate Your Saying Account'
            message = render_to_string('account_activation_email.html', {
                'user': user.userprofile.nickname,
                'domain': 'saying@mashup-dev.org',
                'uid': str(user.pk),
                'token': account_activation_token.make_token(user),
            })

            send_mail(subject, message, 'saying@mashup-dev.org', [user_acc])

            return HttpResponse("register success")
    return HttpResponseBadRequest("required POST method")


@csrf_exempt
def update_profile(request):
    if request.method == "POST":
        upload = request.FILES['image']
        user = UserProfile.objects.get(userid=request.POST['userid'])
        user.user_profile_img = upload
        user.save()
        # data = serializers.serialize("json", User.objects.all())
        # return HttpResponse(data, content_type='application/json')
        return HttpResponse("receive success")
    return HttpResponse("no data")


@csrf_exempt
def list_s3(request):
    get_s3_object()
    return HttpResponse("OK")


def activate(request, userid, token):
    try:
        user = User.objects.get(pk=userid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.users.user_status = 1
        user.save()
        return HttpResponse("user activate complete!")
    else:
        return HttpResponse("there's no user. check user list")
