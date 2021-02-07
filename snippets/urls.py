# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

# 将ViewSets明确的绑定在url上
from snippets.views import SnippetViewSet, UserViewSet


# 将snippet列表页以及创建snippet实例绑定在具体的视图中（list\create视图）
snippet_list = SnippetViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

# 将snippet详情页以及更新snippet实例、删除实例绑定在具体的视图中(retrieve\update\destroy视图）
snippet_detail = SnippetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

# 将高亮代码片段绑定在具体的视图中（自定义的highlight）
snippet_highlight = SnippetViewSet.as_view({
    'get': 'highlight'
})

user_list = UserViewSet.as_view({
    'get': 'list',
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

# urlpatterns = format_suffix_patterns([
#     # 添加API根路径
#     url(r'^$', views.api_root),
#
#     url(r'^snippets/$', views.SnippetList.as_view(), name='snippet-list'),
#     url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view(), name='snippet-detail'),
#
#     # 添加高亮代码片段的路径
#     url(r'snippet/(?P<pk>[0-9]+)/highlight/$', views.SnippetHighLight.as_view(), name='snippet-highlight'),
#
#     url(r'^user/$', views.UserList.as_view(), name='user-list'),
#     url(r'^user/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail')
# ])

# urlpatterns = format_suffix_patterns([
#     # 添加API根路径
#     url(r'^$', views.api_root),
#
#     url(r'^snippets/$', snippet_list, name='snippet-list'),
#     url(r'^snippets/(?P<pk>[0-9]+)/$', snippet_detail, name='snippet-detail'),
#
#     # 添加高亮代码片段的路径
#     url(r'snippet/(?P<pk>[0-9]+)/highlight/$', snippet_highlight, name='snippet-highlight'),
#
#     url(r'^user/$', user_list, name='user-list'),
#     url(r'^user/(?P<pk>[0-9]+)/$', user_detail, name='user-detail')
#
# ])

# urlpatterns += [
#     url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]


# 使用Router重写路由定义
router = DefaultRouter()
router.register(r'snippets', SnippetViewSet)
router.register(r'users', UserViewSet)

schema_view = get_schema_view(title='Pastebin API')

urlpatterns = [
    url(r'^schema', schema_view),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]