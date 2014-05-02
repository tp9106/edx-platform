"""
    The URI scheme for resources is as follows:
        Resource type: /api/{resource_type}
        Specific resource: /api/{resource_type}/{resource_id}

    The remaining URIs provide information about the API and/or module
        System: General context and intended usage
        API: Top-level description of overall API (must live somewhere)
"""

from django.conf.urls import include, patterns, url

from api_manager import system_views

urlpatterns = patterns('',
                       url(r'^$', system_views.ApiDetail.as_view()),
                       url(r'^system$', system_views.SystemDetail.as_view()),
                       url(r'^users/*', include('api_manager.users_urls')),
                       url(r'^groups/*', include('api_manager.groups_urls')),
                       url(r'^sessions/*', include('api_manager.sessions_urls')),
                       url(r'^courses/*', include('api_manager.courses_urls')),
                       )