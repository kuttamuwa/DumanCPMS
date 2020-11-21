# domains

# api endpoints
from django.urls import path
from appconfig import views

from DumanCPMS.urls import cviews


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('filter/', views.DomainFilterView.as_view(), name='filter-domain'),
    path('create/', views.DomainCreateView.as_view(), name='create-domain'),
    path('update/<int:pk>', views.DomainUpdateView.as_view(), name='update-domain'),
    path('read/<int:pk>', views.DomainReadView.as_view(), name='read-domain'),
    path('delete/<int:pk>', views.DomainDeleteView.as_view(), name='delete-domain'),
    path('domains/', views.domains_list, name='domains'),

    # site urls
    path('login/', cviews.LoginUserView.as_view(), name='login'),
    path('logout/', cviews.LogoutUserView.as_view(), name='logout'),
]
