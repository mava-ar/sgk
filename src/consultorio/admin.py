from django.contrib import admin
from django.contrib.auth.models import User, Group
from django_tenants.admin import TenantAdminMixin

from .models import Consultorio, Dominio


class PublicAdminSite(admin.AdminSite):
    site_header = "Kines Public Admin Site"
    site_title = "Kines Public Admin Site"
    index_title = "Welcome to Kines Public Admin Site"

public_admin_site = PublicAdminSite(name='public_admin')

class ConsultorioAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('nombre', 'pagado_hasta', 'plan', 'schema_name')



class DominioAdmin(TenantAdminMixin, admin.ModelAdmin):
    pass


public_admin_site.register(User)
public_admin_site.register(Group)
public_admin_site.register(Consultorio, ConsultorioAdmin)
public_admin_site.register(Dominio, DominioAdmin)
