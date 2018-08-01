# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import rest_framework
from rest_framework.routers import Route, DynamicListRoute, DynamicDetailRoute, SimpleRouter


def get_list_route():
    list_route_data = dict(
        url=r'^{prefix}{trailing_slash}$',
        mapping={
            'get': 'list',
            'post': 'create'
        },
        name='{basename}-list',
        initkwargs={'suffix': 'List'}
    )

    if rest_framework.__version__ > '3.8':
        list_route_data['detail'] = False

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
        initkwargs={'suffix': 'Instance'}
    )

    if rest_framework.__version__ > '3.8':
        detail_route_data['detail'] = False

    return Route(**detail_route_data)


class TusAPIRouter(SimpleRouter):
    routes = [
        # List route.
        get_list_route(),
        # Dynamically generated list routes.
        # Generated using @list_route decorator
        # on methods of the viewset.
        DynamicListRoute(
            url=r'^{prefix}/{methodname}{trailing_slash}$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        ),
        # Detail route.
        get_detail_route(),
        # Dynamically generated detail routes.
        # Generated using @detail_route decorator on methods of the viewset.
        DynamicDetailRoute(
            url=r'^{prefix}/{lookup}/{methodname}{trailing_slash}$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        ),
    ]
