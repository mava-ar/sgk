from django.contrib import admin

from .models import Cobertura, RegistroValorPrestacion


class RegistroValorPrestacionInlineAdmin(admin.StackedInline):
    extra = 1
    can_delete = False
    model = RegistroValorPrestacion
    readonly_fields = ('creado_el', 'fecha_baja', )


@admin.register(Cobertura)
class CoberturaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'telefono', 'email', 'activo')
    search_fields = ('nombre', 'codigo', )

    inlines = [RegistroValorPrestacionInlineAdmin, ]