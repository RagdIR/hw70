import json
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.views.generic import View, DetailView, UpdateView
from django.views.decorators.csrf import ensure_csrf_cookie

from api_v1.serializers import ArticleSerializer
from webapp.models import Article


@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed('Only GET request are allowed')


class ArticleListView(View):
    def get(self, request, *args, **kwargs):
        objects = Article.objects.all()
        slr = ArticleSerializer(objects, many=True)
        return JsonResponse(slr.data, safe=False)


class ArticleCreateView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        slr = ArticleSerializer(data=data)
        if slr.is_valid():
            article = slr.save()
            return JsonResponse(slr.data, safe=False)
        else:
            response = JsonResponse(slr.errors, safe=False)
            response.status_code = 400
            return response

class ArticleView(View):
    def get(self, request, *args, **kwargs):
        article = Article.objects.get(pk=kwargs['pk'])
        slr = ArticleSerializer(article, many=False)
        return JsonResponse(slr.data)


class ArticleUpdateView(View):
    def get(self, request, *args, **kwargs):
        article = Article.objects.get(pk=kwargs['pk'])
        slr = ArticleSerializer(article=article)
        if slr.is_valid():
            article = slr.save()
            return JsonResponse(slr.data, safe=False)
        else:
            response = JsonResponse(slr.errors, safe=False)
            response.status_code = 400
            return response


class ArticleDeleteView(View):
    def get(self, request, *args, **kwargs):
        article = Article.objects.get(pk=kwargs['pk'])
        slr = ArticleSerializer(article=article)
        article = slr.delete()
        return JsonResponse(pk=kwargs['pk'])