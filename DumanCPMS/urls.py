"""DumanCPMS URL Configuration

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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import debug_toolbar

from DumanCPMS import settings
from checkaccount import views as cviews
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),

    # application
    # home page
    path('', include('home.urls')),

    # check account - api and page
    path('checkaccount/', include('checkaccount.urls')),

    # financial Check Up - api
    path('finance_checkup/', include('finance_checkup.urls')),

    path('login/', cviews.LoginUserView.as_view()),
    path('logout/', cviews.LogoutUserView.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
