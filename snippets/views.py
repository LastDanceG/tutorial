# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.http import HttpResponse, Http404

# Create your views here.
from rest_framework import status, generics, permissions, renderers, viewsets
from rest_framework.decorators import api_view, detail_route
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import mixins

from snippets.models import Snippet
from snippets.permissions import IsOwnerReadOnly
from snippets.serializers import SnippetSerializer, UserSerializer


class JsonResponse(HttpResponse):

    """
    响应格式为JSON
    """

    def __init__(self, data, **kwargs):

        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JsonResponse, self).__init__(content, **kwargs)


@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
    """
    列出所有的code snippet，或者创建一个新的snippet
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':

        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    """
    获取，更新或者删除一个code snippet
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # 可以使用request.data， 不需要显示的将请求绑定到指定的类型上，
        # request.data可以处理传入的json请求，或者其它格式的数据也同样可以处理
        # data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


# 重写上面的snippet_list和snippet_detail函数视图（FUNCTION VIEW）,基于类的视图(CLASS VIEW)，
# class SnippetList(APIView):
#     """
#     列出所有的snippets，或者创建一个新的snippet实例
#     """

    # 以下使用mixins重写，list方法，使其可以更好的复用
    # def get(self, request, format=None):
    #
    #     snippets = Snippet.objects.all()
    #     serializer = SnippetSerializer(snippets, many=True)
    #     return Response(serializer.data)
    #
    # def post(self, request, format=None):
    #
    #     serialzer = SnippetSerializer(data=request.data)
    #     if serialzer.is_valid():
    #         serialzer.save()
    #         return Response(serialzer.data, status=status.HTTP_201_CREATED)
    #     return Response(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)


# class SnippetDetail(APIView):
#     """
#     检索、更新或者删除一个snippet实例
#     """
#     def get_object(self, pk):
#         try:
#             snippet = Snippet.objects.get(pk=pk)
#             return snippet
#         except Snippet.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#
#         snippet = self.get_object(pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


#  上面的SnippetList看起来还是和function view差不多。
#  下面会使用mixins来重写SnippetList以及SnippetDetail，可以创建可复用的行为
# class SnippetList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     """
#     查询出所有snippets，或者重新创建一个新的snippet
#     """
#
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class SnippetDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#     def get(self, request, *args, **kwargs):
#
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#
#         return self.destroy(request, *args, **kwargs)


# 使用通用的基于类的视图，使代码更简洁，重写SnippetList, SnippetDetail
class SnippetList(generics.ListCreateAPIView):
    """
    基于generics.ListCreateAPIView的通用视图类，查询所有的snippets，或者创建一个新的snippet实例
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):

        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    基于generics.RetrieveUpdateDestroyAPIView的通用视图类，检索，更新或者删除一个snippet实例
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerReadOnly)


class SnippetHighLight(generics.GenericAPIView):

    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):

        snippet = self.get_object()
        return Response(snippet.highlighted)


class SnippetViewSet(viewsets.ModelViewSet):
    """
    使用viewsets.ModelViewSet替换generics.ListCreateAPIView以及generics.RetrieveUpdateDestroyAPIView的通用视图类
    此视图自动提供`list`, `create`, `retrieve`, `update`和`destroy`操作
    另外还重写一个额外的`highlight`操作
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwagrs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserList(generics.ListAPIView):
    """
    基于generics.ListAPIView的通用视图类，查询所有的用户
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    """
    基于generics.RetrieveAPIView的通用视图类，查询某个用户的实例
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    使用viewsets.ReadOnlyModelViewSet类，替换generics.ListAPIView以及generics.RetrieveAPIView
    改视图自动提供`list`和`detail`操作
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])
def api_root(request, format=None):
    """
    为API创建一个根路径
    """
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })

