from __future__ import absolute_import
from django import forms
from django.forms import CharField, PasswordInput, BooleanField
from django.forms import ValidationError
from django.forms import ModelForm
from django.forms import SelectDateWidget, NumberInput, CheckboxSelectMultiple, Select
from django.forms import inlineformset_factory 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.contrib.auth.models import User
from django.contrib.auth import password_validation 
from django.utils.translation import ugettext, ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from crispy_forms.bootstrap import FormActions
from .models import Profile
from .models import Precio, Amarre 
from .models import Distancia
from .models import Puerto
from .models import Contacto
from .models import Combustible
from .models import Prediccion 
from .models import Embarcacion


class FormContacto(ModelForm):
    class Meta:
        model = Contacto 
        fields = ('domicilio', 'localidad', 'provincia', 'codigo_postal',
                  'pais', 'correo_electronico', 'telefono', 'fax', 'url')
        labels = {
            'domicilio': _('Street'), 
            'localidad': _('City'),
            'provincia': _('Province'),
            'codigo_postal': _('Postal code'),
            'pais': _('Country'),
            'correo_electronico': _('E-mail'),
            'telefono': _('Phone'),
            'fax': _('Fax'),
            'url': _('URL'),
        }

#ContactoFormSet = inlineformset_factory(Puerto, Contacto, form=FormContacto, extra=0)

class UsuarioCreationForm(UserCreationForm):
    DNI = CharField(
        max_length = 13,
        label = ('DNI'),
    )
    gestor_puertos = BooleanField(
        label = ('Port manager'),
        required = False,
    )
    gestor_combustible = BooleanField(
        label = ('Fuel manager'),
        required = False,
    )
    gestor_predicciones = BooleanField(
        label = ('Forecast manager'),
        required = False,
    )

    class Meta:
        model = User
        #fields = ('username', 'first_name', 'last_name', 'email', 'is_superuser', 'groups')
        fields = ('username', 'first_name', 'last_name', 'email', 'is_superuser')


class UsuarioChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(
        label = _("Password"),
        help_text = _("Feature not allowed")
    #                 "this user's password, change password is not allowed")
        )

    class Meta:
        model = User
        exclude = ['is_staff', 'user_permissions', 'date_joined', 'last_login']


class reset_form(forms.Form):
    oldpassword = forms.CharField(max_length = 20, 
        widget=forms.TextInput(attrs={'type':'password', 'placeholder':'your old Password',  'class' : 'span'})
    )
    newpassword1 = forms.CharField(max_length = 20,
        widget=forms.TextInput(attrs={'type':'password', 'placeholder':'New Password',  'class' : 'span'})
    )
    newpassword2 = forms.CharField(max_length = 20, 
        widget=forms.TextInput(attrs={'type':'password', 'placeholder':'Confirm New Password',  'class' : 'span'})
    )

    def clean(self):
        if 'newpassword1' in self.cleaned_data and 'newpassword2' in self.cleaned_data:
            if self.cleaned_data['newpassword1'] != self.cleaned_data['newpassword2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data


class PrecioForm(ModelForm):
    class Meta:
        model = Precio 
        fields = '__all__'
        labels = {
            'nombre': _('Name'), 
            'enero': _('January'),
            'febrero': _('February'),
            'marzo': _('March'),
            'abril': _('April'),
            'mayo': _('May'),
            'junio': _('June'),
            'julio': _('July'),
            'agosto': _('August'),
            'septiembre': _('September'),
            'octubre': _('October'),
            'noviembre': _('November'),
            'diciembre': _('December'),
        }


class AmarreForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AmarreForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-10'
        self.helper.add_input(Submit('order', 'Save', css_class='btn-primary'))

    class Meta:
        model = Amarre 
        fields = '__all__'
        exclude = ['precio_dia']


class DistanciaForm(ModelForm):
    class Meta:
        model = Distancia
        fields = ('origen', 'destino', 'distancia_nmi')


class PuertoForm(ModelForm):
    class Meta:
        model = Puerto
        fields = ('nombre', 'isla', 'latitud', 'longitud', 'amarre', 'duchas', 'informacion')
        labels = {
            'nombre': _('Name'), 
            'isla': _('Island'),
            'latitud': _('Latitude'),
            'longitud': _('Longitude'),
            'amarre': _('Moorings'),
            'duchas': _('Showers'),
            'informacion': _('Information'),
        }
        widgets = {
            'amarre': CheckboxSelectMultiple(),
        }


class CombustibleForm(ModelForm):
    class Meta:
        model = Combustible
        fields = ('nombre', 'tipo', 'precio_litro')
        labels = {
            'nombre': _('Name'), 
            'tipo': _('Type'),
            'precio_litro': _('Price €/l'),
        }
        widgets = {
            'precio_litro': NumberInput(attrs={'min': '0.00',}),
        }


class PrediccionForm(ModelForm):
    class Meta:
        ZONA_CHOICES = (
            ('NO_MA', 'Noroeste Mallorca'),
            ('NE_MA', 'Noreste Mallorca'),
            ('ES_MA', 'Este Mallorca'),
            ('SU_MA', 'Sur Mallorca'),
            ('NO_ME', 'Norte Menorca'),
            ('SU_ME', 'Sur Menorca'),
            ('IBIZA', 'Ibiza'),
        )
        model = Prediccion 
        exclude = ['autor', 'fecha_fin', 'timestamp', 'updated']
        widgets = {
            'zona': Select(choices=ZONA_CHOICES),
            'fecha': SelectDateWidget(),
        }


class EmbarcacionForm(ModelForm):
    class Meta:
        model = Embarcacion 
        fields = ('nombre', 
                  'eslora', 'manga', 'calado', 
                  'motor_num', 'motor_potencia', 'motor_tipo',
                  'motor_consumo', 'motor_combustible', 'velocidad_kn')
        labels = {
            'nombre': _('Name'), 
            'matricula': _('ID.Number'),
            'eslora': _('Length (m)'),
            'manga': _('Beam (m)'),
            'calado': _('Draugth (m)'),
            'motor_num': _('# motor'),
            'motor_potencia': _('Motor CV'),
            'motor_tipo': _('Motor Type'),
            'motor_consumo': _('Consume (l/h)'),
            'motor_combustible': _('Motor fuel'),
            'velocidad_kn': _('Velocity (kn)'),
        }
        widgets = {
            'eslora': NumberInput(attrs={'min': '4.00','max':'15.99',}),
            'manga': NumberInput(attrs={'min': '1.00','max':'5.99',}),
            'calado': NumberInput(attrs={'min': '0.10','max':'3.99',}),
            'motor_num': NumberInput(attrs={'min': '1','max':'4',}),
            'motor_potencia': NumberInput(attrs={'min': '1',}),
            'motor_consumo': NumberInput(attrs={'min': '0',}),
            'velocidad_kn': NumberInput(attrs={'min': '1',}),
        }
