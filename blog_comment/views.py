from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.forms.models import model_to_dict

from blog_comment.models import Comment


@require_GET
def get(request: HttpRequest, post_id: int) -> HttpResponse:
    data = Comment.objects.filter(post_ID=post_id, is_reviewed=True)
    data = [model_to_dict(_) for _ in data]
    return JsonResponse(data, safe=False)


@require_POST
def put(request: HttpRequest, post_id: int) -> HttpResponse:
    return HttpResponse("")
