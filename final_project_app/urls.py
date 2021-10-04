"""final_project_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings

from final_project_cargo.views import Sign_Up_Views, Loginview
from rest_framework_simplejwt.views import TokenRefreshView

from django.conf.urls import url

from django.conf import settings

from django.views.static import serve

urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT}),

    url(r'^static/(?P<path>.*)$', serve,
        {'document_root': settings.STATIC_ROOT}),

    path('', admin.site.urls),

    path('api/Signup/', Sign_Up_Views.as_view(), name='sign_up'),
    path('api/Login/', Loginview.as_view(), name='log_in'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/Send_cargo/', include('final_project_cargo.urls', 'final_project_cargo',)),

    path('api/password_reset/',
         include('django_rest_passwordreset.urls', namespace='password_reset')),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler500 = 'final_project_cargo.views.outside_view_500_error_handler'
