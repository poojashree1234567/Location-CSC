from django.urls import path
from .views import *
from .viewsapi import CountryApiView, get_csrf_token, StateApiView, CityApiView

urlpatterns = [
#country path
    path('',CountryView.as_view(), name='country'),
    path('<str:slug>',CountryView.as_view(), name='country'),
    path('countupdate/<str:slug>/',UpdateCountry.as_view(), name='countupdate'),

#State path
    path('state',StateView.as_view(), name='state'),
    path('state/<str:slug>',StateView.as_view(), name='state'),
    path('stateupdate/<str:slug>/',UpdateState.as_view(), name='stateupdate'),
    path('statedelete/<str:slug>/',DeleteState.as_view(), name='statedelete'),
    path('togglestate/<slug:slug>/', ToggleStateActive.as_view(), name='togglestate'),

# City path
    path('city',CityView.as_view(), name='city'),
    path('city/<str:slug>/', CityView.as_view(), name='city'),
    path('city/<str:countryslug>/<str:stateslug>', CityView.as_view(), name='city'),
    path('cityupdate/<str:slug>/',UpdateCity.as_view(), name='cityupdate'),
    path('citydelete/<str:slug>/',DeleteCity.as_view(), name='citydelete'),
    path('togglecity/<slug:slug>/', ToggleCityActive.as_view(), name='togglecity'),

#Country API path
    path('countryapiview/',CountryApiView.as_view(), name='countryapiview'),
    path('stateapiview/<slug:slug>/',StateApiView.as_view(), name='stateapiview'),
    path('cityapiview/<slug:slug>/',CityApiView.as_view(), name='cityapiview'),

#csrf token
    path('gettoken/', get_csrf_token, name='get-csrf-token'),
]