from decimal import Decimal 
from django.db import models
# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _
from datetime import datetime, timedelta
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from .haversine import *


latitud_baleares = [degMinSec2Deg([38,40,30]),
                    degMinSec2Deg([40,5,48])]
longitud_baleares = [degMinSec2Deg([1,12,47]),
                    degMinSec2Deg([4,19,00])]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    DNI = models.CharField(max_length=13, blank=False)
    gestor_puertos = models.BooleanField(blank = True, default=False)
    gestor_combustible = models.BooleanField(blank = True, default=False)
    gestor_predicciones = models.BooleanField(blank = True, default=False)


class Combustible(models.Model):
    TIPO_COMBUSTIBLE_CHOICES = (
        ('GASL', 'Gasoil'),
        ('GSLN', 'Gasolina'),
    )
    nombre = models.CharField(max_length=50, default = " ")
    tipo = models.CharField(
        max_length=4,
        choices=TIPO_COMBUSTIBLE_CHOICES,
        default='GASL',
    )
    precio_litro = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00)])
    # Timestamp y updated (creado y modificado)
    timestamp = models.DateTimeField(_('TimeStamp'), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, auto_now_add=False)

    def __str__(self):
        return (self.nombre)


class Embarcacion(models.Model):
    TIPO_MOTOR_CHOICES = (
        ('I', 'Intraborda'),
        ('F', 'Foraborda'),
    )
    nombre = models.CharField(max_length=50, default = " ")
    matricula = models.CharField(max_length=40, default = " ")
    # Dimensiones fisicas de la embarcacion en metros con dos decimales
    eslora = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(4.00), MaxValueValidator(15.99)])
    manga = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(1.00), MaxValueValidator(5.99)])
    calado = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0.10), MaxValueValidator(3.99)])
    # Motores
    # TODO: En realidad esto deberia ser una relacion de N a 1 a una 
    # tabla de motores, es decir una embarcacion puede tener muchos motores
    # Numero de motores (1,2,3,4)
    motor_num = models.PositiveIntegerField()
    # Cubicage del motor (centimetros cubicos o hp (horse power))
    motor_potencia = models.PositiveIntegerField()
    # Tipo_motor (Intra o Fora)
    motor_tipo = models.CharField(
        max_length=1,
        choices=TIPO_MOTOR_CHOICES,
        default='F',
    )
    # consumo regimen crucero (litros/hora)
    motor_consumo = models.FloatField()
    # combustible (OneToOne)
    #motor_combustible = models.OneToOneField(Combustible, 
    motor_combustible = models.ForeignKey(Combustible, 
        null = True,
        default = None,
        on_delete = models.SET_NULL
    )
    # Velocidad de crucero en nudos (millas nauticas/hora)
    velocidad_kn = models.PositiveIntegerField(default=1,
        blank=False
    )
    # Propietario
    propietario = models.ForeignKey(User, 
        null=True, 
        default = None,
        on_delete=models.SET_NULL
    )
    # Timestamp y updated (creado y modificado)
    timestamp = models.DateTimeField(_('TimeStamp'), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, auto_now_add=False)
    
    def __str__(self):
        return (self.nombre)


class Contacto(models.Model):
    domicilio = models.TextField(_('street'), blank=True)
    localidad = models.CharField(_('city'), max_length=200, blank=True)
    provincia = models.CharField(_('province'), max_length=200, blank=True)
    codigo_postal = models.CharField(_('postal code'), max_length=10, blank=True)
    pais = models.CharField(_('country'), max_length=100, blank=True)
    correo_electronico = models.EmailField(_('email'), blank=True)
    telefono_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    telefono = models.CharField(_('phone'), max_length=16, validators=[telefono_regex], blank=True)
    fax = models.CharField(max_length=16, validators=[telefono_regex], blank=True)
    url = models.URLField(blank=True)
    # Timestamp y updated (creado y modificado)
    timestamp = models.DateTimeField(_('TimeStamp'), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, auto_now_add=False)

    def __str__(self):
        return "%s (%s)" % (self.localidad, self.domicilio)


class Precio(models.Model):
    nombre = models.CharField(_('name'),
        max_length=50, 
        default = " ")
    enero = models.DecimalField(_('January'), max_digits=4, decimal_places=2, default=10.00)
    febrero = models.DecimalField(_('February'), max_digits=4, decimal_places=2, default=10.00)
    marzo = models.DecimalField(_('March'), max_digits=4, decimal_places=2, default=10.00)
    abril = models.DecimalField(_('April'), max_digits=4, decimal_places=2, default=10.00)
    mayo = models.DecimalField(_('May'), max_digits=4, decimal_places=2, default=10.00)
    junio = models.DecimalField(_('June'), max_digits=4, decimal_places=2, default=10.00)
    julio = models.DecimalField(_('July'), max_digits=4, decimal_places=2, default=10.00)
    agosto = models.DecimalField(_('August'), max_digits=4, decimal_places=2, default=10.00)
    septiembre = models.DecimalField(_('September'), max_digits=4, decimal_places=2, default=10.00)
    octubre = models.DecimalField(_('October'), max_digits=4, decimal_places=2, default=10.00)
    noviembre = models.DecimalField(_('November'), max_digits=4, decimal_places=2, default=10.00)
    diciembre = models.DecimalField(_('December'), max_digits=4, decimal_places=2, default=10.00)
    # Timestamp y updated (creado y modificado)
    timestamp = models.DateTimeField(_('TimeStamp'), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, auto_now_add=False)

    def __str__(self):
        return (self.nombre)


class Amarre(models.Model):
    nombre = models.CharField(_('name'),
        max_length=50, 
        default = " ")
    eslora = models.DecimalField(_('length'), max_digits=4, decimal_places=2)
    manga = models.DecimalField(_('beam'), max_digits=4, decimal_places=2)
    agua = models.BooleanField(_('water'), default=True)
    electricidad = models.BooleanField(_('electricity'), default=True)
    precio_dia = models.ForeignKey(Precio, 
        null = True,
        default = None,
        on_delete=models.SET_NULL)
    #puertos = models.ManyToManyField(Puerto)
    info = models.TextField(
         _('information'),
         max_length=160,
         blank=True
    )
    # Timestamp y updated (creado y modificado)
    timestamp = models.DateTimeField(_('TimeStamp'), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, auto_now_add=False)

    def __str__(self):
        return (self.nombre + ',' + str(self.eslora) + 'x' + str(self.manga))


class Puerto(models.Model):
    TIPO_ISLA_CHOICES = (
        ('MA', 'Mallorca'),
        ('ME', 'Menorca'),
        ('IB', 'Ibiza'),
        ('FO', 'Formentera'),
    )
    nombre = models.CharField(_('name'),max_length=50, default = " ")
    # isla de las Islas Baleares 
    isla = models.CharField(_('island'),
        max_length=2,
        choices=TIPO_ISLA_CHOICES,
        default='MA',
    )
    # Coordenadas geograficas
    latitud = models.FloatField(_('latitude'), 
                                validators= [MinValueValidator(latitud_baleares[0]), MaxValueValidator(latitud_baleares[1])]
                               )
    longitud = models.FloatField(_('longitude'),
                                validators= [MinValueValidator(longitud_baleares[0]), MaxValueValidator(longitud_baleares[1])]
                               )
    #temporadas
    #amarres
    amarre = models.ManyToManyField(Amarre,
        null = True,
        blank = True,
        default = None
    )
    # Tiene rampa o no el puerto
    rampa = models.BooleanField(default=False)
    duchas = models.BooleanField(default=False)
    # Informacion adicional del puerto
    informacion = models.TextField(_('information'),
         max_length=160,
         blank=True
    )
    # Foto del puerto
    imagen = models.ImageField(_('image'), upload_to='images', blank=True, null=True)
    # Informacion de contacto del puerto (puede no tener)
    contacto = models.OneToOneField(Contacto, 
        null = True,
        blank = True,
        default = None,
        on_delete = models.SET_NULL
    )
    # Timestamp y updated (creado y modificado)
    timestamp = models.DateTimeField(_('TimeStamp'), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, auto_now_add=False)
    
    def __str__(self):
        return (self.nombre)


class Distancia(models.Model):
    #origen = models.OneToOneField(Puerto,
    origen = models.ForeignKey(Puerto,
        null = True,
        on_delete = models.SET_NULL,
        related_name=_('source')
    )    
    #destino = models.OneToOneField(Puerto,
    destino = models.ForeignKey(Puerto,
        null = True,
        on_delete = models.SET_NULL,
        related_name=_('destination')
    )
    distancia_nmi = models.DecimalField(_('distance_nmi'), max_digits=5, decimal_places=2, default=Decimal('00.00'))
    # Timestamp y updated (creado y modificado)
    timestamp = models.DateTimeField(_('TimeStamp'), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, auto_now_add=False)
    
    def __str__(self):
        return (self.origen.nombre + '-' + self.destino.nombre)


class Prediccion(models.Model):
    TIPO_ESTADO_DE_LA_MAR_CHOICES = (
        ('0', 'Calma'),
        ('1', 'Rizada'),
        ('2', 'Marejadilla'),
        ('3', 'Marejada'),
        ('4', 'Fuerte Marejada'),
        ('5', 'Gruesa'),
        ('6', 'Muy Gruesa'),
        ('7', 'Arbolada'),
        ('8', 'Montañosa'),
        ('9', 'Enorme'),
    )
    TIPO_ORIGEN_CHOICES = (
        ('PE', 'Personal'),
        ('AE', 'Aemet'),
    )
    TIPO_ZONA_CHOICES = (
        ('NO_MA', 'Noroeste Mallorca'),
        ('NE_MA', 'Noreste Mallorca'),
        ('ES_MA', 'Este Mallorca'),
        ('SU_MA', 'Sur Mallorca'),
        ('CN_ME', 'Canal de Menorca'),
        ('NO_ME', 'Norte Menorca'),
        ('SU_ME', 'Sur Menorca'),
        ('CN_IB', 'Canal de Ibiza'),
        ('IBIZA', 'Ibiza'),
        ('FORMN', 'Formentera'),
    )
    TIPO_DIRECCION_CHOICES = (
        ('NT', 'Norte'),
        ('NE', 'Noreste'),
        ('ES', 'Este'),
        ('SE', 'Sureste'),
        ('SU', 'Sur'),
        ('SO', 'Suroeste'),
        ('OE', 'Oeste'),
        ('NO', 'Noroeste'),
    )
    nombre = models.CharField(_('name'), 
         max_length=80,
         blank=True)
    #TODO: Esto debe ser tipo CHOICE
    zona = models.CharField(_('zone'), 
        max_length=5,
        choices=TIPO_ZONA_CHOICES,
        default='NO_MA',
    )
    origen = models.CharField(_('source'),
        max_length=2,
        choices=TIPO_ORIGEN_CHOICES,
        default='PE',
    )
    #TODO: Futura conexion a opendata.aemet.es
    prediccion = models.TextField(_('forecast'),
         max_length=160,
         blank=True
    )
    #TODO: Esto debe ser tipo CHOICE
    estado_de_la_mar = models.CharField(
        max_length=1,
        choices=TIPO_ESTADO_DE_LA_MAR_CHOICES,
        default='0',
    )
    #direccion = models.CharField(
    #    max_length=2,
    #    choices=TIPO_DIRECCION_CHOICES,
    #    default='SU',
    #)
    fecha_inicio = models.DateField(
        _('start_date'),
        default=datetime.now,
        blank=False,
    )
    dias = models.PositiveIntegerField(
        _('days'),
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        default=1
    )
    fecha_fin = models.DateField(
        _('end_date'),
        default=datetime.now,
        blank=True,
    )
    autor = models.ForeignKey(User, 
        null = True,
        default = None,
        on_delete=models.SET_NULL)
    # Timestamp y updated (creado y modificado)
    timestamp = models.DateTimeField(_('TimeStamp'), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, auto_now_add=False)

    def __str__(self):
        return (self.nombre)

    def save(self, *args, **kwargs):
        self.fecha_fin = self.fecha_inicio + timedelta(days=self.dias)
        super(Prediccion, self).save(*args, **kwargs) 
