import json

from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET, require_POST
from django.forms.models import model_to_dict

from blog_comment.models import Comment


@require_GET
def get(request: HttpRequest, post_id: int) -> HttpResponse:
    ret = []
    for data in Comment.objects.filter(post_ID=post_id, is_reviewed=True):
        d = model_to_dict(data, fields=['author', 'email', 'content', ])
        d['time'] = data.time.strftime('%Y-%m-%d %H:%M:%S')
        ret.append(d)
    return JsonResponse(ret, safe=False, json_dumps_params={"ensure_ascii": False})


@require_POST
def put(request: HttpRequest, post_id: int) -> HttpResponse:
    try:
        data = json.loads(request.body.decode())
        author = str(data['author'])
        email = str(data['email'])
        content = str(data['content'])
        is_reviewed = Comment.objects.filter(email=email, is_reviewed=True).exists()
        Comment(post_ID=post_id,
                author=author,
                email=email,
                content=content,
                is_reviewed=is_reviewed).save()
        return HttpResponse("OK")
    except Exception as e:
        return HttpResponseBadRequest(str(e))
