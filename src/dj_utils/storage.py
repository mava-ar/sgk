import os

from django.db import connection
from django.core.exceptions import SuspiciousOperation
from django.core.files.storage import FileSystemStorage
from django.utils._os import safe_join


class MultiTenantStorageMixin(object):
    """
    Mixin that can be combined with other Storage backends to colocate media
    for all tenants in distinct subdirectories.
    Using rewriting rules at the reverse proxy we can determine which content
    gets served up, while any code interactions will account for the multiple
    tenancy of the project.
    """
    def path(self, name):
        """
        Look for files in subdirectory of MEDIA_ROOT using the tenant's
        domain_url value as the specifier.
        """
        if name is None:
            name = ''
        # import ipdb; ipdb.set_trace()
        try:
            domain = connection.tenant.domain_url
            if domain in name:
                location = self.location
            else:
                location = safe_join(self.location, domain)
        except AttributeError:
            location = self.location
        try:
            path = safe_join(location, name)
        except ValueError:
            raise SuspiciousOperation(
                "Attempted access to '%s' denied." % name)
        return os.path.normpath(path)


class MultiTenantStorage(MultiTenantStorageMixin, FileSystemStorage):
    """
    Implementation that extends core Django's FileSystemStorage.
    """
