# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.routers import Route, DynamicRoute, SimpleRouter


def get_list_route():
    list_route_data = dict(
        url=r'^{prefix}{trailing_slash}$',
        mapping={
            'get': 'list',
            'post': 'create'
        },
        name='{basename}-list',
        detail=False,
        initkwargs={'suffix': 'List'}
    )

    return Route(**list_route_data)


def get_detail_route():
    detail_route_data = dict(
        url=r'^{prefix}/{lookup}{trailing_slash}$',
        mapping={
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
            'head': 'info'
        },
        name='{basename}-detail',
        detail=False,
        initkwargs={'suffix': 'Instance'}
    )

    return Route(**detail_route_data)


class TusAPIRouter(SimpleRouter):
    routes = [
        # List route.
        get_list_route(),
        # Dynamically generated list routes.
        # Generated using @list_route decorator
        # on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{methodname}{trailing_slash}$',
            name='{basename}-{methodnamehyphen}',
            detail=False,
            initkwargs={}
        ),
        # Detail route.
        get_detail_route(),
        # Dynamically generated detail routes.
        # Generated using @detail_route decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{lookup}/{methodname}{trailing_slash}$',
            name='{basename}-{methodnamehyphen}',
            detail=True,
            initkwargs={}
        ),
    ]
