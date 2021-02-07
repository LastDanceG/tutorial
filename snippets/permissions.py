# -*- coding: utf-8 -*-
from rest_framework import permissions


class IsOwnerReadOnly(permissions.BasePermission):
    """
    自定义权限只允许对象的所属者编辑它
    """

    def has_object_permission(self, request, view, obj):
        """
        读取权限允许任何请求
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        # 只有改snippet的所属者才有写权限
        return obj.owner == request.user
