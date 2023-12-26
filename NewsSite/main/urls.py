from .views import AboutView, ContactView, MainView, SearchResultsView
# from django.contrib.auth.views import LogoutView
# from django.conf import settings
from django.urls import path, include


urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('', include('news.urls')),
    path('', include('users.urls')),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),

    # path('signout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='signout',),


]