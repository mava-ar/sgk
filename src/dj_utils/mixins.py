

class ShowInfoMixin(object):
    field_info = ()

    @property
    def show_info(self):
        """
        Retorna una diccionario con información. Si no se especifica field_info,
        se utilizará todos los campos.
        :return:
        """
        if not self.field_info:
            self.field_info = [f.name for f in self._meta.get_fields()]
        data = []
        for f in self.field_info:
            if hasattr(self, f):
                item = self._meta.get_field(f)
                data.append({'title': item.verbose_name.title(),
                             'field': item,
                             'value': getattr(self, f)})
        return data
