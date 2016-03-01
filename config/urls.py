# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

#from rest_framework import routers
from rest_framework_nested import routers

from gmp.authentication import views as users_views
from gmp.filestorage import views as filestorage_views
from gmp.certificate import views as certificate_views
#from gmp.departments import views as departments_views


user_router = routers.SimpleRouter()
user_router.register(r'user', users_views.EmployeeViewset)

certificates_router = routers.NestedSimpleRouter(user_router, r'user', lookup='user')
certificates_router.register(r'certificates', certificate_views.CertificateViewset)

router_files = routers.SimpleRouter()
router_files.register('file', filestorage_views.FileViewset)

#router_certificates = routers.SimpleRouter()
#router_certificates.register('certificates', certificate_views.CertificateViewset)

urlpatterns = [
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name="about"),

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, include(admin.site.urls)),

    # User management
    url(r'^users/', include("gmp.users.urls", namespace="users")),
    url(r'^accounts/', include('allauth.urls')),

    # Your stuff: custom urls includes go here
    url(r'^api/', include(user_router.urls)),
    url(r'^api/', include(certificates_router.urls)),
    url(r'^api/department', users_views.DepartmentList.as_view()),
    url(r'^api/login', users_views.LoginView.as_view(), name='login'),
    url(r'^api/logout', users_views.LogoutView.as_view(), name='logout'),
    # Files manage views
    url(r'^api/', include(router_files.urls)),
    url(r'^api/upload', filestorage_views.FileUploadView.as_view(), name='files'),
    url(r'^.*$', TemplateView.as_view(template_name='home.html'), name="home"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception("Bad Request!")}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception("Permissin Denied")}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception("Page not Found")}),
        url(r'^500/$', default_views.server_error),
    ]
