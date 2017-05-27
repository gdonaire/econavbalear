from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from amarreapp.models import Profile 
from amarreapp.models import Combustible 
from amarreapp.models import Embarcacion 
from amarreapp.models import Contacto 
from amarreapp.models import Precio 
from amarreapp.models import Amarre 
from amarreapp.models import Puerto
from amarreapp.models import Distancia 
from amarreapp.models import Prediccion 

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile 
    can_delete = False
    verbose_name_plural = 'profile'
    fields = ('DNI', 
        'gestor_puertos', 
        'gestor_combustible', 
        'gestor_predicciones') 

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )


class CombustibleAdmin(admin.ModelAdmin):
    list_display = ('nombre','tipo', 'precio_litro',)
    readonly_fields = ('timestamp', 'updated',)


class EmbarcacionAdmin(admin.ModelAdmin):
    list_display = ('nombre','propietario', 'eslora', 'manga')
    readonly_fields = ('timestamp', 'updated',)


class ContactoAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp', 'updated',)


class PrecioAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Precio._meta.fields if field.name not in ['id', 'timestamp', 'updated']]
    list_filter = ('nombre',)
    ordering = ('-updated',)
    readonly_fields = ('timestamp', 'updated',)


class AmarreAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'eslora', 'manga',)
    list_filter = ('nombre','eslora','manga')
    ordering = ('-updated',)
    readonly_fields = ('timestamp', 'updated',)


class AmarresInline(admin.TabularInline):
    model = Puerto.amarre.through 


class PuertoAdmin(admin.ModelAdmin):
    list_display = ('nombre','latitud','longitud',)
    inlines = [
        AmarresInline,
    ]
    list_filter = ('nombre',)
    #ordering = ('-updated','id')
    ordering = ('id',)
    readonly_fields = ('timestamp', 'updated',)


class DistanciaAdmin(admin.ModelAdmin):
    list_display = ('origen', 'destino', 'distancia_nmi',)
    list_filter = ('origen','destino',)
    readonly_fields = ('timestamp', 'updated',)


class PrediccionAdmin(admin.ModelAdmin):
    list_display = ('nombre','zona', 'fecha_inicio', 'fecha_fin', 'estado_de_la_mar',)
    readonly_fields = ('timestamp', 'updated',)
    exclude = ('fecha_fin',)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Combustible, CombustibleAdmin)
admin.site.register(Embarcacion, EmbarcacionAdmin)
admin.site.register(Contacto, ContactoAdmin)
admin.site.register(Precio, PrecioAdmin)
admin.site.register(Amarre, AmarreAdmin)
admin.site.register(Puerto, PuertoAdmin)
admin.site.register(Distancia, DistanciaAdmin)
admin.site.register(Prediccion, PrediccionAdmin)
