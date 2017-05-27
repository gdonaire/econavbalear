"""amarres URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Interfaz administrativa
    url(r'^admin/', admin.site.urls),
    # Aplicacion Amarreapp 
    url(r'^$', include('amarreapp.urls')),
    url(r'^econavbalear/', include('amarreapp.urls')),
    # Django-registration-redux
    # gestion de login
    #url(r'^accounts/login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='auth_login'), 
    url(r'^accounts/', include('registration.backends.simple.urls')),
    # While in the registration.backends.default.urls it also provides 
    # the functions for activating the account in a two stage process:
    # url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),

# The Django Registration Redux package provides the machinery for numerous
# functions. In the registration.backend.simple.urls, it provides:
#
#    registration -> /accounts/register/
#    registration complete -> /accounts/register/complete
#    login -> /accounts/login/
#    logout -> /accounts/logout/
#    password change -> /password/change/
#    password reset -> /password/reset/
#
#While in the registration.backends.default.urls it also provides the functions for activating the account in a two stage process:
#
#    activation complete (used in the two-step registration) -> activate/complete/
#    activate (used if the account actiona fails) -> activate/<activation_key>/
#    activation email (notifies the user an activation email has been sent out)
#
#            activation email body (a text file, that contains the activation email text)
#            activation email subject (a text file, that contains the subject line of the activation email)
#
#Now the catch. While Django Registration Redux provides all this functionality, it does not provide the templates. So we need to provide the templates associated with each view.
]
