# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

from rest_framework_nested import routers

from gmp.authentication import views as user_views
from gmp.filestorage import views as filestorage_views
from gmp.certificate import views as certificate_views
from gmp.departments import views as department_views
from gmp.engines import views as engine_views
from gmp.reports import views as report_views
from gmp.inspections import views as inspections_views
from gmp.containers import views as containers_views
from gmp.history import views as history_views


departments = routers.SimpleRouter()
departments.register(r'department', department_views.DepartmentViewset)

measurers = routers.NestedSimpleRouter(departments, r'department', lookup='department')
measurers.register(r'measurer', department_views.MeasurerViewset)

users = routers.NestedSimpleRouter(departments, r'department', lookup='department')
users.register(r'user', user_views.EmployeeViewset)

certificates = routers.NestedSimpleRouter(users, r'user', lookup='user')
certificates.register(r'certificates', certificate_views.CertificateViewset)

files = routers.SimpleRouter()
files.register('file', filestorage_views.FileViewset)

engines = routers.SimpleRouter()
engines.register('engine', engine_views.EngineViewset)

organizations = routers.SimpleRouter()
organizations.register('organization', inspections_views.OrganizationViewset)

lpus = routers.NestedSimpleRouter(organizations, r'organization', lookup='organization')
lpus.register(r'lpu', inspections_views.LPUViewset)

tclasses = routers.SimpleRouter()
tclasses.register('tclass', engine_views.TClassViewset)

connection_types = routers.SimpleRouter()
connection_types.register('connection_types', engine_views.ConnectionTypesViewset)

containers = routers.SimpleRouter()
containers.register('container', containers_views.ContainerViewset)

history = routers.SimpleRouter()
history.register(r'history_input', history_views.InputViewset, base_name='input')

urlpatterns = [
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name="about"),

    #url(r'^contact/$', user_views.ContactFormView.as_view()),

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, include(admin.site.urls)),

    # User management
    url(r'^users/', include("gmp.users.urls", namespace="users")),
    #url(r'^accounts/', include('allauth.urls')),

    # /api/user/
    url(r'^api/', include(users.urls)), 

    # /api/user/<username>/certificate/
    url(r'^api/', include(certificates.urls)),

    # /api/department/
    url(r'^api/', include(departments.urls)),

    # /api/department/<id>/measurer/
    url(r'^api/', include(measurers.urls)),

    # /api/history_input/
    url(r'^api/', include(history.urls)),

    # /api/engine/
    url(r'^api/', include(engines.urls)),

    # /api/file/
    url(r'^api/', include(files.urls)),

    url(r'^media/', filestorage_views.file_response, name='file_download'),

    # /api/organization/
    url(r'^api/', include(organizations.urls)),

    # /api/organization/<id>/lpu/
    url(r'^api/', include(lpus.urls)),

    # /api/tclass/
    url(r'^api/', include(tclasses.urls)),

    # /api/connection_types/
    url(r'^api/', include(connection_types.urls)),

    # /api/containers/
    url(r'^api/', include(containers.urls)),

    # Additional routes
    url(r'^api/login', user_views.LoginView.as_view(), name='login'),
    url(r'^api/logout', user_views.LogoutView.as_view(), name='logout'),
    url(r'^api/upload', filestorage_views.FileUploadView.as_view(), name='files'),

    # Report route
    url(r'^report/$', report_views.create_report, name="report"),
    #url(r'^report/$', report_views.create_report_debug, name="report"),

    # Pass-through route
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
