import json

from django.core import validators
from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.forms.models import model_to_dict

from .models import Comment

SESSION_AUTH = "auth"
CONFIG_PASSWORD = "123"


def get(request: HttpRequest, post_id: int) -> HttpResponse:
    ret = []
    for data in Comment.objects.order_by('time').filter(post_ID=post_id):
        if data.is_reviewed:
            d = model_to_dict(data, fields=['author', 'content', ])
        else:
            d = {'author': "审核中", 'content': "审核中"}
        d['time'] = data.time.strftime('%Y-%m-%d %H:%M:%S')
        if not data.is_reviewed:
            d['author'] = "审核中"
            d['content'] = "审核中"
        ret.append(d)
    return JsonResponse(ret, safe=False, json_dumps_params={"ensure_ascii": False})


@require_POST
def put(request: HttpRequest, post_id: int) -> HttpResponse:
    try:
        data = json.loads(request.body.decode())
        author = str(data['author'])
        email = str(data['email'])
        content = str(data['content'])
        try:
            validators.validate_email(email)
            is_reviewed = Comment.objects.filter(email=email, is_reviewed=True).exists()
        except ValidationError:
            is_reviewed = False
        Comment(post_ID=post_id,
                author=author,
                email=email,
                content=content,
                is_reviewed=is_reviewed).save()
        return HttpResponse("OK")
    except Exception as e:
        return HttpResponseBadRequest(str(e))


def accept(request: HttpRequest, comment_id: int) -> HttpResponse:
    if not request.session.get(SESSION_AUTH):
        return HttpResponseForbidden()
    comment = Comment.objects.get(id=comment_id)
    comment.is_reviewed = True
    comment.save()
    return HttpResponse("审核成功")


def reject(request: HttpRequest, comment_id: int) -> HttpResponse:
    if not request.session.get(SESSION_AUTH):
        return HttpResponseForbidden()
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return HttpResponse("删除成功")


def admin(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        password = request.POST['password']
        if password is None or len(password) == 0:
            return render(request, "LoginPage.html", {"msg": "empty password"})
        elif password == CONFIG_PASSWORD:
            request.session[SESSION_AUTH] = True
            request.session.set_expiry(0)
        else:
            return render(request, "LoginPage.html", {"msg": "incorrect password"})
    if not request.session.get(SESSION_AUTH):
        return render(request, "LoginPage.html")
    return render(request, "AdminPage.html", {"records": Comment.objects.filter(is_reviewed=False)})
