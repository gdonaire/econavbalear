from __future__ import absolute_import
from django.forms import CharField, PasswordInput, BooleanField
from django.forms import ValidationError
from django.forms import ModelForm
from django.forms import SelectDateWidget, NumberInput, CheckboxSelectMultiple
from django.forms import inlineformset_factory 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation 
from django.utils.translation import ugettext, ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from crispy_forms.bootstrap import FormActions
from .models import Profile
from .models import Precio, Amarre 
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
    class Meta:
        model = User
        exclude = ['is_staff', 'user_permissions', 'date_joined', 'last_login']


class PrecioForm(ModelForm):
    class Meta:
        model = Precio 
        fields = '__all__'


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


class PuertoForm(ModelForm):
    class Meta:
        model = Puerto
        fields = ('nombre', 'isla', 'latitud', 'longitud', 'amarre', 'duchas', 'informacion')
        labels = {
            'nombre': _('Name'), 
            'isla': _('Island'),
            'latitud': _('Lattitude'),
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
        widgets = {
            'precio_litro': NumberInput(attrs={'min': '0.00',}),
        }


class PrediccionForm(ModelForm):
    class Meta:
        model = Prediccion 
        exclude = ['autor', 'fecha_fin', 'timestamp', 'updated']
        widgets = {
            'fecha': SelectDateWidget(),
        }


class EmbarcacionForm(ModelForm):
    class Meta:
        model = Embarcacion 
        fields = ('nombre', 'matricula',
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
