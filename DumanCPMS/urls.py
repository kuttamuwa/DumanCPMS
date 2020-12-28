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

import debug_toolbar
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from DumanCPMS import siteviews as sviews

from DumanCPMS import settings
# from checkaccount import views as cviews

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),

    # application
    # home page
    path('', include('home.urls')),

    # check account - api and page
    path('checkaccount/', include('checkaccount.urls')),

    # risk analysis - page
    path('risk_analysis/', include('risk_analysis.urls')),

    # financial Check Up - api
    path('finance_checkup/', include('finance_checkup.urls')),

    path('login/', sviews.LoginUserView.as_view(), name='login'),
    path('logout/', sviews.LogoutUserView.as_view(), name='logout'),
    path('register/', sviews.register_user, name='register'),

    # appconfig
    path('appconfig/', include('appconfig.urls')),

    # dashboard
    path('dashboard/', include('dashboard.urls')),

    # example - modal
    path('modalex/', include('modalex.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
