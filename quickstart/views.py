# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User, Group
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from quickstart.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):

    """
    允许用户查看或者编辑的API路径
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):

    """
    允许组查看或者编辑的API路径
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
