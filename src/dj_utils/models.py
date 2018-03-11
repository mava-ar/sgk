from os.path import join

from django.db import models, connection
from django.utils.text import slugify


class BaseModel(models.Model):
    """
    Todos los modelos deben heredar de esta clase.

    """
    class Meta:
        abstract = True

    creado_el = models.DateTimeField(verbose_name=u"Fecha de creación",
            auto_now_add=True)
    modificado_el = models.DateTimeField(verbose_name=u"Fecha de modificación",
            auto_now=True)


def uploadTenantFilename(basepath, instance, filename):
    """
    Helper to upload files in FileField fields with multitenant support

    To use in FiledField argument 'upload_to':
        upload_to=partial(uploadFilename, basepath )
    Where basepath is the path where the file will save.

    @param basepath: Base path to save the file (list or string)
    @param instance: Model instance
    @param filename: The filename that was originally given to the file.
    @return: string with file path.
    """
    if isinstance(basepath, str):
        # Converts to lowercase, removes non-word characters
        # (alphanumerics and underscores) and converts spaces
        # to hyphens. Also strips leading and trailing whitespace.
        basepath = slugify(basepath)
    else:
        # if basepath is a list
        basepath = join(*map(slugify, basepath))
    return join(connection.tenant.domain_url, basepath, filename)
