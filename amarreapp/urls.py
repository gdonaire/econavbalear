from django.conf.urls import url
from django.views.i18n import set_language
from . import views
from .views import ListUsuarios, CreateUsuario, EditUsuario, DeleteUsuario
from .views import ListPrecios, CreatePrecio, EditPrecio, DeletePrecio
from .views import ListAmarres, CreateAmarre, EditAmarre, DeleteAmarre
from .views import ListPuertos, CreatePuerto, EditPuerto, DeletePuerto
from .views import ListCombustibles, CreateCombustible, EditCombustible, DeleteCombustible
from .views import ListPredicciones, CreatePrediccion, EditPrediccion, DeletePrediccion
from .views import ListEmbarcaciones, CreateEmbarcacion, EditEmbarcacion, DeleteEmbarcacion

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^usuario$', ListUsuarios.as_view(), name='list_usuarios'),
    url(r'^usuario/create$', CreateUsuario.as_view(), name='create_usuario'),
    url(r'^usuario/edit/(?P<pk>\d+)/$', EditUsuario.as_view(), name='edit_usuario'),
    url(r'^usuario/delete/(?P<pk>\d+)/$', DeleteUsuario.as_view(), name='delete_usuario'),
    url(r'^precio$', ListPrecios.as_view(), name='list_precios'),
    url(r'^precio/create$', CreatePrecio.as_view(), name='create_precio'),
    url(r'^precio/edit/(?P<pk>\d+)/$', EditPrecio.as_view(), name='edit_precio'),
    url(r'^precio/delete/(?P<pk>\d+)/$', DeletePrecio.as_view(), name='delete_precio'),
    url(r'^amarre$', ListAmarres.as_view(), name='list_amarres'),
    url(r'^amarre/create$', CreateAmarre.as_view(), name='create_amarre'),
    url(r'^amarre/edit/(?P<pk>\d+)/$', EditAmarre.as_view(), name='edit_amarre'),
    url(r'^amarre/delete/(?P<pk>\d+)/$', DeleteAmarre.as_view(), name='delete_amarre'),
    url(r'^puerto$', ListPuertos.as_view(), name='list_puertos'),
    url(r'^puerto/create$', CreatePuerto.as_view(), name='create_puerto'),
    url(r'^puerto/edit/(?P<pk>\d+)/$', EditPuerto.as_view(), name='edit_puerto'),
    url(r'^puerto/delete/(?P<pk>\d+)/$', DeletePuerto.as_view(), name='delete_puerto'),
    url(r'^combustible$', ListCombustibles.as_view(), name='list_combustibles'),
    url(r'^combustible/create$', CreateCombustible.as_view(), name='create_combustible'),
    url(r'^combustible/edit/(?P<pk>\d+)/$', EditCombustible.as_view(), name='edit_combustible'),
    url(r'^combustible/delete/(?P<pk>\d+)/$', DeleteCombustible.as_view(), name='delete_combustible'),
    url(r'^prediccion$', ListPredicciones.as_view(), name='list_predicciones'),
    url(r'^prediccion/create$', CreatePrediccion.as_view(), name='create_prediccion'),
    url(r'^prediccion/edit/(?P<pk>\d+)/$', EditPrediccion.as_view(), name='edit_prediccion'),
    url(r'^prediccion/delete/(?P<pk>\d+)/$', DeletePrediccion.as_view(), name='delete_prediccion'),
    url(r'^embarcacion$', ListEmbarcaciones.as_view(), name='list_embarcaciones'),
    url(r'^embarcacion/create$', CreateEmbarcacion.as_view(), name='create_embarcacion'),
    url(r'^embarcacion/edit/(?P<pk>\d+)/$', EditEmbarcacion.as_view(), name='edit_embarcacion'),
    url(r'^embarcacion/delete/(?P<pk>\d+)/$', DeleteEmbarcacion.as_view(), name='delete_embarcacion'),
    url(r'^reserva$', views.search_mooring, name='search_mooring'),
]
