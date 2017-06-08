from __future__ import absolute_import
from django import forms 
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect 
from django.core.urlresolvers import reverse 
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from django.contrib.auth.models import Group
from django.utils import translation, timezone
from django.utils.translation import ugettext as _
#from django.utils.translation import (
#    LANGUAGE_SESSION_KEY, check_for_language, get_language, to_locale, activate,
#)
from django.utils.decorators import method_decorator 
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.
#from django.views.generic.list import ListView
from vanilla import CreateView, DeleteView, ListView, UpdateView
from extra_views import CreateWithInlinesView, InlineFormSet
from decimal import Decimal, getcontext
from datetime import timedelta
from django.http import HttpResponse
from django.template import RequestContext
from django.forms import modelformset_factory
from django.forms import inlineformset_factory
from .decorators import group_required 
from .forms import FormContacto
from .forms import UsuarioCreationForm, UsuarioChangeForm, reset_form
from .forms import PrecioForm, AmarreForm
#from .forms import DistanciaFormSet 
from .forms import PuertoForm
from .forms import DistanciaForm
from .forms import CombustibleForm
from .forms import PrediccionForm
from .forms import EmbarcacionForm
from django.contrib.auth.models import User
from .models import Profile 
from .models import Distancia, Precio 
from .models import Precio, Amarre, Puerto, Combustible
from .models import Prediccion 
from .models import Embarcacion
from .haversine import *

# Constantes
latitud_baleares = [degMinSec2Deg([38,40,30]),
                    degMinSec2Deg([40,5,48])]
longitud_baleares = [degMinSec2Deg([1,12,47]),
                    degMinSec2Deg([4,19,00])]
                    
FACTOR_CORRECCION_NO_NAVEGAR = 0.0

@login_required()
def index(request):
    context_dict = {}
    # Return response back to the user, updating any cookies that need changed. 
    response = render(request, 'index.html', context_dict)                      
    return response  


def set_language_beta(request):
    next = request.META.get('HTTP_REFERER', None) or '/'
    response = HttpResponseRedirect(next)
    lang_code = request.POST.get('language', None)
    translation.activate(lang_code)
    request.session[LANGUAGE_SESSION_KEY] = lang_code
    return response


def set_language_old(request):
    next = request.META.get('HTTP_REFERER', None) or '/'
    response = HttpResponseRedirect(next)
    if request.method == 'POST':
        lang_code = request.POST.get('language', None)
        if lang_code and check_for_language(lang_code):
            activate(lang_code)
            if hasattr(request, 'session'):
                request.session[LANGUAGE_SESSION_KEY] = lang_code
            else:
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code,
                    )
    return response


@method_decorator([login_required, user_passes_test(lambda u: u.is_superuser)], name='dispatch')
class ListUsuarios(ListView):
    model = User 
    template_name='usuarios.html'

    def post(self, request, *args, **kwargs):
        order = request.POST.get('order')
        pk = request.POST.get('pk')
        if (order == 'add'):
            return HttpResponseRedirect(reverse('create_usuario'))
        elif (order == 'edit'):
            return HttpResponseRedirect(reverse('edit_usuario', kwargs={'pk':pk}))
        elif (order == 'delete'):
            return HttpResponseRedirect(reverse('delete_usuario', kwargs={'pk':pk}))


@method_decorator([login_required, user_passes_test(lambda u: u.is_superuser)], name='dispatch')
class CreateUsuario(CreateView):
    model = User 
    form_class = UsuarioCreationForm
    template_name = 'usuario_add.html'
    success_url=reverse_lazy('list_usuarios')

    def get(self, request, *args, **kwargs):
        form = UsuarioCreationForm()
        print('CreateUsuario get')
        print(form)
        context_dict = {'form': form}
        # Return response back to the user, updating any cookies that need changed. 
        response = render(request, self.template_name, context_dict) 
        return response  

    def post(self, request, *args, **kwargs):
        order = request.POST.get('order')
        data = request.POST
        print('CreateUsuario post')
        print(order)
        print(data)
        if (order == 'Save'):
            form = UsuarioCreationForm(data)
            print(form)
            if form.is_valid():
                usuario = form.save()
                perfil = Profile(user = usuario)
                perfil.DNI = form.cleaned_data.get("DNI")
                perfil.gestor_puertos = form.cleaned_data.get("gestor_puertos")
                perfil.gestor_combustible = form.cleaned_data.get("gestor_combustible")
                perfil.gestor_predicciones = form.cleaned_data.get("gestor_predicciones")
                perfil.save()
                usuario.save()
                if perfil.gestor_puertos:
                    g = Group.objects.get(name='gestor_puerto')
                    g.user_set.add(usuario)
                if perfil.gestor_combustible:
                    g = Group.objects.get(name='gestor_combustible')
                    g.user_set.add(usuario)
                if perfil.gestor_predicciones:
                    g = Group.objects.get(name='gestor_prediccion')
                    g.user_set.add(usuario)
                    
            else:
                context_dict = {'form': form}
                response = render(request, self.template_name, context_dict) 
                return response  
        return HttpResponseRedirect(self.get_success_url())
 

@method_decorator([login_required, user_passes_test(lambda u: u.is_superuser)], name='dispatch')
class EditUsuario(UpdateView):
    model = User 
    form_class = UsuarioChangeForm
    success_url=reverse_lazy('list_usuarios')


@method_decorator([login_required, user_passes_test(lambda u: u.is_superuser)], name='dispatch')
class DeleteUsuario(DeleteView):
    model = User 
    success_url=reverse_lazy('list_usuarios')

@login_required
def change_password(request):
    if request.method == 'POST':
        order = request.POST.get('order')
        form = reset_form(request.POST)
        if (order is not None) and (order == 'Change'):
            if form.is_valid():
                newpassword=form.cleaned_data['newpassword1'],
                username=request.user.username
                password=form.cleaned_data['oldpassword']
                user = authenticate(username=username, password=password)
                if user is not None:
                    user.set_password(newpassword)
                    user.save()
                    return render(request, 'registration/password_change_done.html')
                else:
                    return render(request, 'registration/password_change_form.html', {'error':'You have entered wrong password','form': form,})
        else:
           return render(request, 'registration/password_change_form.html',{'error':'You have entered wrong password','form': form,})
    else:
        form = reset_form()
        context_dict = {'form': form}
        response = render(request, 'registration/password_change_form.html', context_dict) 
        return response


@method_decorator([login_required, group_required('gestor_puerto')], name='dispatch')
class ListPrecios(ListView):
    model = Precio 
    template_name='precios.html'

    def post(self, request, *args, **kwargs):
        order = request.POST.get('order')
        pk = request.POST.get('pk')
        if (order == 'add'):
            return HttpResponseRedirect(reverse('create_precio'))
        elif (order == 'edit'):
            return HttpResponseRedirect(reverse('edit_precio', kwargs={'pk':pk}))
        elif (order == 'delete'):
            return HttpResponseRedirect(reverse('delete_precio', kwargs={'pk':pk}))


@method_decorator([login_required, group_required('gestor_puerto')], name='dispatch')
class CreatePrecio(CreateView):
    model = Precio 
    form_class = PrecioForm 
    success_url=reverse_lazy('list_precios')
    
    def post(self, request, *args, **kwargs):
        order = request.POST.get('order')
        print('CreatePrecio order %s' % order)
        if (order == 'cancel'):
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(CreatePrecio, self).post(request, *args, **kwargs)


@method_decorator([login_required, group_required('gestor_puerto')], name='dispatch')
class EditPrecio(UpdateView):
    model = Precio 
    form_class = PrecioForm 
    success_url=reverse_lazy('list_precios')


@method_decorator([login_required, group_required('gestor_puerto')], name='dispatch')
class DeletePrecio(DeleteView):
    model = Precio 
    success_url=reverse_lazy('list_precios')


@method_decorator([login_required, group_required('gestor_puerto')], name='dispatch')
class ListAmarres(ListView):
    model = Amarre 
    template_name='amarres.html'

    def post(self, request, *args, **kwargs):
        order = request.POST.get('order')
        pk = request.POST.get('pk')
        if (order == 'add'):
            return HttpResponseRedirect(reverse('create_amarre'))
        elif (order == 'edit'):
            return HttpResponseRedirect(reverse('edit_amarre', kwargs={'pk':pk}))
        elif (order == 'delete'):
            return HttpResponseRedirect(reverse('delete_amarre', kwargs={'pk':pk}))


@method_decorator([login_required, group_required('gestor_puerto')], name='dispatch')
class CreateAmarre(CreateView):
    model = Amarre
    form_class = AmarreForm 
    success_url=reverse_lazy('list_amarres')

    def get(self, request, *args, **kwargs):
        form = AmarreForm
        precios = Precio.objects.all()
        context_dict = {'form': form, 'list_precios': precios}
        # Return response back to the user, updating any cookies that need changed. 
        response = render(request, 'amarre_add.html', context_dict) 
        return response  

    def post(self, request, *args, **kwargs):
        order = request.POST.get('order')
        if (order == 'Save'):
            data = request.POST
            form = AmarreForm(data)
            opcionPrecio = request.POST.get('opcionPrecio') 
            if form.is_valid() and opcionPrecio:
                cd = form.cleaned_data
                amarre = Amarre()
                amarre.nombre = cd.get('nombre')
                amarre.eslora = cd.get('eslora')
                amarre.manga = cd.get('manga')
                amarre.agua = cd.get('agua')
                amarre.electricidad = cd.get('electricidad')
                amarre.precio_dia = Precio.objects.get(pk=opcionPrecio)
                amarre.save()
        return HttpResponseRedirect(reverse('list_amarres'))


@method_decorator([login_required, group_required('gestor_puerto')], name='dispatch')
class EditAmarre(UpdateView):
    model = Amarre
    form_class = AmarreForm 
    success_url=reverse_lazy('list_amarres')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        print(self.object)
        form = AmarreForm(instance=self.object)
        print(form)
        precios = Precio.objects.all()
        context_dict = {'form': form, 'list_precios': precios, 'object': self.object }
        # Return response back to the user, updating any cookies that need changed. 
        response = render(request, 'amarre_edit.html', context_dict) 
        return response  
    
    def post(self, request, *args, **kwargs):
        order = request.POST.get('order')
        if (order == 'Save'):
            data = request.POST
            form = AmarreForm(data)
            opcionPrecio = request.POST.get('opcionPrecio') 
            if form.is_valid() and opcionPrecio:
                cd = form.cleaned_data
                amarre = self.get_object()
                amarre.nombre = cd.get('nombre')
                amarre.eslora = cd.get('eslora')
                amarre.manga = cd.get('manga')
                amarre.agua = cd.get('agua')
                amarre.electricidad = cd.get('electricidad')
                amarre.precio_dia = Precio.objects.get(pk=opcionPrecio)
                amarre.save()
        return HttpResponseRedirect(reverse('list_amarres'))


@method_decorator([login_required, group_required('gestor_puerto')], name='dispatch')
class DeleteAmarre(DeleteView):
    model = Amarre 
    success_url=reverse_lazy('list_amarres')


@method_decorator([login_required, group_required('gestor_puerto')], name='dispatch')
class ListDistancias(ListView):
    model = Distancia 
    template_name='distancias.html'

    def post(self, request, *args, **kwargs):
        order = request.POST.get('order')
        pk = request.POST.get('pk')
        if (order == 'add'):
            return HttpResponseRedirect(reverse('create_distancia'))
        elif (order == 'edit'):
            return HttpResponseRedirect(reverse('edit_distancia', kwargs={'pk':pk}))
        elif (order == 'delete'):
            return HttpResponseRedirect(reverse('delete_distancia', kwargs={'pk':pk}))


@method_decorator([login_required, group_required('gestor_puerto')], name='dispatch')
class CreateDistancia(CreateView):
    model = Distancia
    form_class = DistanciaForm
    success_url=reverse_lazy('list_distancias')


@method_decorator([login_required, group_required('gestor_puerto')], name='dispatch')
class EditDistancia(UpdateView):
    model = Distancia
    form_class = DistanciaForm 
    success_url=reverse_lazy('list_distancias')


@method_decorator([login_required, group_required('gestor_puerto')], name='dispatch')
class DeleteDistancia(DeleteView):
    model = Distancia 
    success_url=reverse_lazy('list_distancias')


@method_decorator([login_required, group_required('gestor_puerto')], name='dispatch')
class ListPuertos(ListView):
    model = Puerto 
    template_name='puertos.html'

    def post(self, request, *args, **kwargs):
        order = request.POST.get('order')
        pk = request.POST.get('pk')
        if (order == 'add'):
            return HttpResponseRedirect(reverse('create_puerto'))
        elif (order == 'edit'):
            return HttpResponseRedirect(reverse('edit_puerto', kwargs={'pk':pk}))
        elif (order == 'delete'):
            return HttpResponseRedirect(reverse('delete_puerto', kwargs={'pk':pk}))

class DistanciasInline(InlineFormSet):
    model = Distancia
    fields = ['destino', 'distancia_nmi']


@method_decorator([login_required, group_required('gestor_puerto')], name='dispatch')
class CreatePuerto(CreateWithInlinesView):
    model = Puerto 
    context_object_name = 'puerto'
    fields = ['nombre', 'isla', 'latitud', 'longitud', 'amarre', 'duchas', 'informacion']
    template_name = 'puerto_add.html'
    success_url=reverse_lazy('list_puertos')
    
    def get(self, request, *args, **kwargs):
        data = {'isla':'Mallorca'}
        puerto_form = PuertoForm(data, prefix="port")
        contacto_form = FormContacto(prefix="contact")
        amarres = Amarre.objects.all()
        # Numero de formularios extra para las distancias...tantos como puertos exista
        extra=Puerto.objects.count()
        initial_data = []
        for puerto in Puerto.objects.all():
            initial_data.append({'destino':puerto})
        DistanciasInlineFormSet = inlineformset_factory(Puerto, Distancia, fk_name='origen', fields=('destino','distancia_nmi',), extra=extra)
        formset = DistanciasInlineFormSet(instance=None, initial=initial_data, prefix='origen')
        context_dict = {'puerto_form': puerto_form, 'contacto_form': contacto_form, 'amarres': amarres, 'inlines':formset, 'extra':extra}
        # Return response back to the user, updating any cookies that need changed. 
        response = render(request, 'puerto_add.html', context_dict)                      
        return response  
    
    def post(self, request, *args, **kwargs):
        order = request.POST.get('order')
        if (order == 'Save'):
            data = request.POST
            puerto_form = PuertoForm(data, prefix="port")
            contacto_form = FormContacto(data, prefix="contact")
            extra = int(float(request.POST['extra']))
            DistanciasInlineFormSet = inlineformset_factory(Puerto, Distancia, fk_name='origen', fields=('destino','distancia_nmi',), extra=extra)
            distancias_formset = DistanciasInlineFormSet(data, request.FILES, instance=None, prefix='origen')
            if not puerto_form.is_valid():
                print('PUERTO NOOOOOOOOOOOOOOOOOO VALIDO')
            if not contacto_form.is_valid():
                print('CONTACTO NOOOOOOOOOOOOOOOOOO VALIDO')
            if not distancias_formset.is_valid():
                print('FORMSET NOOOOOOOOOOOOOOOOOO VALIDO')
            if puerto_form.is_valid() and contacto_form.is_valid() and distancias_formset.is_valid():
                contacto = contacto_form.save()
                cd = puerto_form.cleaned_data
                #puerto = Puerto()
                puerto = puerto_form.save(commit=False)
                #puerto.nombre = cd.get('nombre')
                #puerto.isla = cd.get('isla')
                #puerto.latitud = cd.get('latitud')
                #puerto.longitud = cd.get('longitud')
                #puerto.rampa = False
                puerto.contacto = contacto
                puerto.save()
                for distancia_form in distancias_formset:
                    origen = puerto
                    destino = distancia_form.cleaned_data.get('destino')
                    distancia_nmi = distancia_form.cleaned_data.get('distancia_nmi')
                    if (destino is not None) and (distancia_nmi is not None) and (distancia_nmi > 0):
                    #print('Origen')
                    #print(origen)
                    #print('Destino')
                    #print(destino)
                    #print('Distancia_nmi')
                    #print(distancia_nmi)
                        dist = Distancia(origen=puerto, destino=destino, distancia_nmi=distancia_nmi)
                        dist.save()
        return HttpResponseRedirect(reverse('list_puertos'))


@method_decorator([login_required, group_required('gestor_puerto')], name='dispatch')
class EditPuerto(UpdateView):
    model = Puerto 
    form_class = PuertoForm
    success_url=reverse_lazy('list_puertos')


#@method_decorator([login_required, permission_required('amarreapp.delete_puerto')], name='dispatch')
@method_decorator([login_required, group_required('gestor_puerto')], name='dispatch')
class DeletePuerto(DeleteView):
    model = Puerto 
    success_url=reverse_lazy('list_puertos')


@method_decorator([login_required, group_required('gestor_combustible')], name='dispatch')
class ListCombustibles(ListView):
    model = Combustible 
    template_name='combustibles.html'

    def post(self, request, *args, **kwargs):
        order = request.POST.get('order')
        pk = request.POST.get('pk')
        if (order == 'add'):
            return HttpResponseRedirect(reverse('create_combustible'))
        elif (order == 'edit'):
            return HttpResponseRedirect(reverse('edit_combustible', kwargs={'pk':pk}))
        elif (order == 'delete'):
            return HttpResponseRedirect(reverse('delete_combustible', kwargs={'pk':pk}))


@method_decorator([login_required, group_required('gestor_combustible')], name='dispatch')
class CreateCombustible(CreateView):
    model = Combustible 
    form_class = CombustibleForm
    success_url=reverse_lazy('list_combustibles')


@method_decorator([login_required, group_required('gestor_combustible')], name='dispatch')
class EditCombustible(UpdateView):
    model = Combustible 
    form_class = CombustibleForm
    success_url=reverse_lazy('list_combustibles')


@method_decorator([login_required, group_required('gestor_combustible')], name='dispatch')
class DeleteCombustible(DeleteView):
    model = Combustible 
    success_url=reverse_lazy('list_combustibles')


@method_decorator([login_required, group_required('gestor_prediccion')], name='dispatch')
class ListPredicciones(ListView):
    model = Prediccion 
    template_name='predicciones.html'
    
    def post(self, request, *args, **kwargs):
        order = request.POST.get('order')
        pk = request.POST.get('pk')
        if (order == 'add'):
            return HttpResponseRedirect(reverse('create_prediccion'))
        elif (order == 'edit'):
            return HttpResponseRedirect(reverse('edit_prediccion', kwargs={'pk':pk}))
        elif (order == 'delete'):
            return HttpResponseRedirect(reverse('delete_prediccion', kwargs={'pk':pk}))


@method_decorator([login_required, group_required('gestor_prediccion')], name='dispatch')
class CreatePrediccion(CreateView):
    model = Prediccion
    form_class = PrediccionForm
    success_url=reverse_lazy('list_predicciones')
    
    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super(CreatePrediccion, self).form_valid(form)


@method_decorator([login_required, group_required('gestor_prediccion')], name='dispatch')
class EditPrediccion(UpdateView):
    model = Prediccion
    form_class = PrediccionForm
    success_url=reverse_lazy('list_predicciones')


@method_decorator([login_required, group_required('gestor_prediccion')], name='dispatch')
class DeletePrediccion(DeleteView):
    model = Prediccion
    success_url=reverse_lazy('list_predicciones')


@method_decorator(login_required, name='dispatch')
class ListEmbarcaciones(ListView):
    model = Embarcacion
    template_name='embarcaciones.html'

    def get_queryset(self):
        return Embarcacion.objects.filter(propietario=self.request.user)
    
    def post(self, request, *args, **kwargs):
        order = request.POST.get('order')
        pk = request.POST.get('pk')
        if (order == 'add'):
            return HttpResponseRedirect(reverse('create_embarcacion'))
        elif (order == 'edit'):
            return HttpResponseRedirect(reverse('edit_embarcacion', kwargs={'pk':pk}))
        elif (order == 'delete'):
            return HttpResponseRedirect(reverse('delete_embarcacion', kwargs={'pk':pk}))


@method_decorator(login_required, name='dispatch')
class CreateEmbarcacion(CreateView):
    model = Embarcacion
    form_class = EmbarcacionForm
    success_url=reverse_lazy('list_embarcaciones')

    def form_valid(self, form):
        form.instance.propietario = self.request.user
        return super(CreateEmbarcacion, self).form_valid(form)
    

@method_decorator(login_required, name='dispatch')
class EditEmbarcacion(UpdateView):
    model = Embarcacion
    form_class = EmbarcacionForm
    success_url=reverse_lazy('list_embarcaciones')


@method_decorator(login_required, name='dispatch')
class DeleteEmbarcacion(DeleteView):
    model = Embarcacion
    success_url=reverse_lazy('list_embarcaciones')


@login_required
def search_mooring(request):
    class SearchMooringForm(forms.Form):
        dias = forms.IntegerField(label=_('Days'), min_value=1, max_value=5)
        fecha_entrada = forms.DateField(
                                        label=_('Start Date'),
                                        initial=timezone.now().date(),
                                        widget=forms.SelectDateWidget())
        latitud = forms.FloatField(label=_('Lat.'),
                                  error_messages={'min_value':'Outside Balearic Islands Region'},
                                  widget=forms.NumberInput(attrs={'min':'38.675000', 'max':'40.096666', 'step':'0.000001'})
                                  )
        longitud = forms.FloatField(label=_('Long.'),
                                  error_messages={'min_value':'Outside Balearic Islands Region'},
                                  widget=forms.NumberInput(attrs={'min':'1.213055', 'max':'4.316666', 'step':'0.000001'})
                                  )
        embarcacion = forms.ModelChoiceField(label=_('Boat'),
            queryset=Embarcacion.objects.filter(propietario=request.user)
        )


    if request.method == 'POST':
        #form = MooringSearchForm(request.POST)
        form = SearchMooringForm(request.POST or None)
        if form.is_valid():
            posicion_barca = [form.cleaned_data.get('latitud'), form.cleaned_data.get('longitud')]
            embarcacion = form.cleaned_data.get('embarcacion')
            boats = Embarcacion.objects.all()
            #embarcacion = get_object_or_404(boats, pk=embarcacion_id)
            dias = form.cleaned_data.get('dias')
            #fecha_reserva_mes = int(form.cleaned_data.get('fecha_entrada_month'))
            fecha_entrada = form.cleaned_data.get('fecha_entrada')
            print('posicion_barca: [%f, %f]' % (posicion_barca[0], posicion_barca[1]))
            print('embarcacion: %s' % embarcacion.nombre)
            print('dias: %d' % dias)
            print('fecha_entrada: %d' % fecha_entrada.month)
            tabla_resultados = []
            # Mirar si hay puertos con amarres para nuestra embarcacion
            puertos = []
            puertos = localizar_puertos_con_amarre(embarcacion)
            print('Puertos con amarre')
            print(puertos)
            if puertos:
                puerto_distancia = []
                puerto_distancia = calcular_distancias_puerto(posicion_barca, puertos)
                puertos =[]
                distancias_nmi = []
                for x in puerto_distancia:
                    puertos.append(x[0])
                    distancias_nmi.append(x[1])
                print('Distancias puerto (nmi)')
                print(distancias_nmi)
                # Calcular los costes....
                factor_correccion = []
                for i in range(len(puerto_distancia)):
                    puerto = puertos[i]
                    posicion_puerto = [puerto.latitud, puerto.longitud]
                    distancia_nmi = distancias_nmi[i]
                    factor = calcular_factor_correccion_meteo(posicion_puerto, distancia_nmi, embarcacion, fecha_entrada)
                    factor_correccion.append(factor)
                print('Factores correcion')
                print(factor_correccion)
                # Costes de navegacion
                costes_navegacion = []
                for i in range(len(distancias_nmi)):
                    distancia = distancias_nmi[i]
                    factor_correccion_meteo = factor_correccion[i]
                    coste_nav = calcular_coste_navegacion(distancia, embarcacion)
                    print('Coste_nav %f' % coste_nav)
                    if (factor_correccion_meteo > 0.0):
                        coste_nav = coste_nav / factor_correccion_meteo 
                        print('Coste_nav %f' % coste_nav)
                    costes_navegacion.append(coste_nav)
                # Costes de amarres
                costes_amarres = []
                for puerto in puertos:
                    # Aunque el puerto tenga mas amarres que cumplan el criterio ...
                    # ordenamos por tamaño de eslora y despues manga y nos quedamos con el primero
                    amarre = puerto.amarre.all().order_by('eslora').order_by('manga')[0]
                    coste_amarre = calcular_coste_amarre(dias, fecha_entrada, amarre)
                    costes_amarres.append(coste_amarre)
                # Costes totales
                # Tabla de resultados
                for i in range(len(costes_amarres)):
                    # Solo agregamos los resultados que no se desaconsejan por mal tiempo....
                    if (factor_correccion[i] != FACTOR_CORRECCION_NO_NAVEGAR):
                        puerto = puertos[i]
                        distancia_nmi = distancias_nmi[i]
                        coste_nav = costes_navegacion[i]
                        coste_amarre = costes_amarres[i]
                        coste_total = coste_nav + coste_amarre
                        tabla_resultados.append([puerto.nombre, 
                                                 float("{0:.2f}".format(distancia_nmi)), 
                                                 float("{0:.2f}".format(coste_nav)), 
                                                 float("{0:.2f}".format(coste_amarre)),
                                                float("{0:.2f}".format(coste_total))
                                                ])
            print(tabla_resultados)
            # Ordenar por coste total
            tabla_resultados.sort(key=lambda x:x[4])
            print(tabla_resultados)
            # Coger los primeros cinco resultados
            tabla_truncada = tabla_resultados[0:5]
            print(tabla_truncada)
            #context_dict = {'object_list': tabla_resultados}
            context_dict = {'object_list': tabla_truncada}
            # Return response back to the user, updating any cookies that need changed. 
            response = render(request, 'resultado_amarre.html', context_dict)                      
            return response  
    else:
        form = SearchMooringForm()
        #form = MooringSearchForm()
    return render(request, 'buscar_amarre.html', {'form': form}) 


def localizar_puertos_con_amarre(embarcacion):
    puertos=Puerto.objects.filter(amarre__eslora__gte=embarcacion.eslora, amarre__manga__gte=embarcacion.manga).distinct()
    return puertos

def calcular_distancias_puerto(posicion, puertos):
    # localizar el puerto mas cercano
    puerto = puertos[0]
    distancia_menor_nmi = km2nm(points2distance(posicion, [puerto.latitud, puerto.longitud]))
    resultado = [puerto, distancia_menor_nmi]
    for puerto in puertos[1:]:
        # Calcular Distancia
        distancia = km2nm(points2distance(posicion, [puerto.latitud, puerto.longitud]))
        if distancia < distancia_menor_nmi:
            distancia_menor_nmi = distancia
            resultado = [puerto, distancia_menor_nmi]
    # Distancias desde el puerto mas cercano a los otros puertos encontrados
    resultados = []
    resultados.append(resultado)
    puerto_mas_cercano = resultado[0]
    for puerto in puertos:
        if puerto != puerto_mas_cercano:
            if (Distancia.objects.filter(origen__nombre=puerto_mas_cercano.nombre, destino__nombre = puerto.nombre)):
                distancia_a_puerto_mas_cercano = (float(Distancia.objects.filter(origen__nombre=puerto_mas_cercano.nombre, destino__nombre = puerto.nombre).get().distancia_nmi))
            elif (Distancia.objects.filter(origen__nombre=puerto.nombre, destino__nombre=puerto_mas_cercano.nombre)):
                distancia_a_puerto_mas_cercano = (float(Distancia.objects.filter(origen__nombre=puerto.nombre, destino__nombre = puerto_mas_cercano.nombre).get().distancia_nmi))
            else:
                # No se ha introducido distancia entre los puestos .... coger distancia en linia recta
                distancia_a_puerto_mas_cercano = km2nm(points2distance([puerto_mas_cercano.latitud, puerto_mas_cercano.longitud], [puerto.latitud, puerto.longitud]))
            distancia = distancia_a_puerto_mas_cercano + distancia_menor_nmi
            resultado = [puerto, distancia]
            resultados.append(resultado)
    resultados.sort(key=lambda x:x[1])
    return resultados
                   
 
def calcular_factor_correccion_meteo(posicion, distancia_nmi, embarcacion, fecha_reserva):
    zona_puerto = localizar_zona_navegacion(posicion)
    dias_de_navegacion = (distancia_nmi/embarcacion.velocidad_kn)/24
    fecha_inicio_navegacion = fecha_reserva - timedelta(days=dias_de_navegacion)
    factor = 1.00
    # Prediccion con fecha de inicio de prediccion entre el inicio de la navegacion y
    # la llegada a puerto
    prediccion = Prediccion.objects.filter(zona = zona_puerto, fecha_inicio__range=[fecha_inicio_navegacion, fecha_reserva]).distinct()
    if prediccion:
        # Nos quedamos con la primera prediccion
        prediccion = prediccion[0]
        if prediccion.get_estado_de_la_mar_display() == 'Calma':
            factor = 1.1
        elif prediccion.get_estado_de_la_mar_display() == 'Rizada':
            factor = 1.0
        elif prediccion.get_estado_de_la_mar_display() == 'Marejadilla':
            factor = 0.9
        elif prediccion.get_estado_de_la_mar_display() == 'Marejada':
            factor = 0.7
        else:
            # Cualquier otra prediccion devolver un valor exagerado
            factor = FACTOR_CORRECCION_NO_NAVEGAR
    else:
        # Prediccion con fecha de fin entre el inicio de la navegacion
        # y la llegada a puerto
        prediccion = Prediccion.objects.filter(zona = zona_puerto, fecha_fin__range=[fecha_inicio_navegacion, fecha_reserva]).distinct()
        if prediccion:
            # Nos quedamos con la primera prediccion
            prediccion = prediccion[0]
            if prediccion.get_estado_de_la_mar_display() == 'Calma':
                factor = 1.1
            elif prediccion.get_estado_de_la_mar_display() == 'Rizada':
                factor = 1.0
            elif prediccion.get_estado_de_la_mar_display() == 'Marejadilla':
                factor = 0.9 
            elif prediccion.get_estado_de_la_mar_display() == 'Marejada':
                factor = 0.7
            else:
                # Cualquier otra prediccion devolver un valor exagerado
                factor = (MAXIMO_FACTOR_CORRECCION + 0.1)
    # Si no hay prediccion no afecta 
    print('posicion_puerto: [%f, %f]' % (posicion[0], posicion[1]))
    print('Zona puerto %s' % zona_puerto)
    print('dias de navegacion %d' % dias_de_navegacion)
    print('fecha de navegacion: ')
    print(fecha_inicio_navegacion)
    print('fecha de reserva ')
    print(fecha_reserva)
    print('factor correcion %f' % factor)
    return factor


def calcular_coste_navegacion(distancia_nmi, embarcacion):
    # Calcular coste de navegacion a puertos
    # tiempo de navegacion (hr) = distancia_millas / (velocidad_kn * factor_de_correccion)
    # coste_navegacion = tiempo_de_navegacion * consumo_motor_litros/hora * numero_motores * precio_combustible/litro
    tiempo_de_navegacion = distancia_nmi/embarcacion.velocidad_kn
    coste_navegacion = tiempo_de_navegacion * (embarcacion.motor_consumo * embarcacion.motor_num * float(embarcacion.motor_combustible.precio_litro))
    return coste_navegacion

    
def localizar_zona_navegacion(posicion):
    latitud = posicion[0]
    longitud = posicion[1]
    if ((longitud >= 1.00) and (latitud >= 38.20) and
        ((longitud <= 4.35) and (latitud <= 40.15))):
        # Zona de Baleares
        if (((longitud >= 1.00) and (longitud <= 2.00)) and
            ((latitud >= 38.20) and (latitud <= 39.13))):
            # Zona de Ibiza 
            return 'IBIZA'
        if (((longitud > 2.00) and (longitud <= 3.36)) and
            ((latitud >= 39.00) and (latitud <= 40.11))):
            # Zona de Mallorca 
            if (longitud <= 3.05):
                if (latitud > 39.35):
                    return 'NO_MA'
                return 'SU_MA'
            else:
                if (latitud > 39.43):
                    return 'NE_MA'
                return 'ES_MA'
        if (((longitud > 3.36) and (longitud <= 4.35)) and
            ((latitud >= 39.48) and (latitud <= 40.15))):
            # Zona de Menorca 
            if (latitud > 40.02):
                return 'NO_ME'
            return 'SU_ME'
    return 'NO_IB' 


def calcular_coste_amarre(dias, fecha_reserva, amarre):
    # Calcular coste de pernocta
    # el precio por dia va en funcion del mes
    # coste_noches = precio_dia_amarre * numero_dias
    fecha_reserva_mes = fecha_reserva.month
    precios = amarre.precio_dia
    if (fecha_reserva_mes == 1):
        precio_dia = precios.enero 
    if (fecha_reserva_mes == 2):
        precio_dia = precios.febrero
    if (fecha_reserva_mes == 3): 
        precio_dia = precios.marzo
    if (fecha_reserva_mes == 4):
        precio_dia = precios.abril
    if (fecha_reserva_mes == 5):
        precio_dia = precios.mayo
    if (fecha_reserva_mes == 6):
        precio_dia = precios.junio
    if (fecha_reserva_mes == 7):
        precio_dia = precios.julio
    if (fecha_reserva_mes == 8):
        precio_dia = precios.agosto
    if (fecha_reserva_mes == 9):
        precio_dia = precios.septiembre
    if (fecha_reserva_mes == 10):
        precio_dia = precios.octubre
    if (fecha_reserva_mes == 11):
        precio_dia = precios.noviembre
    if (fecha_reserva_mes == 12):
        precio_dia = precios.diciembre
    coste_amarre = float(precio_dia) * dias
    return coste_amarre


def show_zonas_puerto():
    for puerto in Puerto.objects.all():
        posicion = [puerto.latitud, puerto.longitud]
        zona = localizar_zona_navegacion(posicion)
        print('Puerto: %s, Posicion (%f, %f), Zona %s' % (puerto.nombre, puerto.latitud, puerto.longitud, zona))

