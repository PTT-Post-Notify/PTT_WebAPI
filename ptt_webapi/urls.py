"""ptt_webapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from ptt_linker.views import *
from ptt_linker.views.boardClass import *

swagger = get_schema_view(
    openapi.Info(
        title="PTT WebAPI",
        description="Provide RESTFul API to access ptt.cc",
        default_version='v1',
        terms_of_service="https://github.com/MakotoAtsu/PTT_WebAPI",
        contact=openapi.Contact(
            name="MakotoAtsu",
            url="https://github.com/MakotoAtsu"
        ),
    ),
    public=True
)

urlpatterns = [
    path('', swagger.with_ui()),
    # path('admin/', admin.site.urls),
    path('board/<str:bid>/articles', get_board_articles),
    path('board/<str:bid>/articles/query', search_board_articles),
    path('board/<str:bid>/article/<str:aid>', get_article_detail),
    path('class/', get_all_class),
    path('class/<int:cls>', get_particular_class)
    #
]

# provide static file in wsgi
urlpatterns += staticfiles_urlpatterns()
