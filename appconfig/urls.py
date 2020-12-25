# domains

# api endpoints
from django.urls import path
from appconfig import views

from DumanCPMS import siteviews as sviews


urlpatterns = [
    path('', views.Index.as_view(), name='app-index'),

    # domains crud
    path('domains/', views.DomainIndex.as_view(), name='domain-index'),
    path('domains/filter/', views.DomainFilterView.as_view(), name='filter-domain'),
    path('domains/create/', views.DomainCreateView.as_view(), name='create-domain'),
    path('domains/update/<int:pk>', views.DomainUpdateView.as_view(), name='update-domain'),
    path('domains/read/<int:pk>', views.DomainReadView.as_view(), name='read-domain'),
    path('domains/delete/<int:pk>', views.DomainDeleteView.as_view(), name='delete-domain'),
    path('domains/all', views.domains_list, name='domains-all'),

    # subtypes crud
    path('subtypes/', views.SubtypeIndex.as_view(), name='subtype-index'),
    path('subtypes/filter/', views.SubtypeFilterView.as_view(), name='filter-subtype'),
    path('subtypes/create/', views.SubtypeCreateView.as_view(), name='create-subtype'),
    path('subtypes/update/<int:pk>', views.SubtypeUpdateView.as_view(), name='update-subtype'),
    path('subtypes/read/<int:pk>', views.SubtypeReadView.as_view(), name='read-subtype'),
    path('subtypes/delete/<int:pk>', views.SubtypeDeleteView.as_view(), name='delete-subtype'),
    path('subtypes/all', views.subtypes_list, name='subtypes'),
    
    # risk dataset config crud
    path('riskconfig/', views.RiskDataIndex.as_view(), name='rd-index'),
    path('riskconfig/filter/', views.RiskConfigFilterView.as_view(), name='filter-riskconfig'),
    path('riskconfig/create/', views.RiskConfigCreateView.as_view(), name='create-riskconfig'),
    path('riskconfig/update/<int:pk>', views.RiskConfigUpdateView.as_view(), name='update-riskconfig'),
    path('riskconfig/read/<int:pk>', views.RiskConfigReadView.as_view(), name='read-riskconfig'),
    path('riskconfig/delete/<int:pk>', views.RiskConfigDeleteView.as_view(), name='delete-riskconfig'),
    path('riskconfig/all', views.riskconfigs_list, name='riskconfigs'),

    # site urls
    path('login/', sviews.LoginUserView.as_view(), name='login'),
    path('logout/', sviews.LogoutUserView.as_view(), name='logout'),
]
