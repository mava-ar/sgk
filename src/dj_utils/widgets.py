from datetimewidget.widgets import DateWidget, TimeWidget


class FechaWidget(DateWidget):
    def __init__(self, **kwargs):
        use10n = kwargs.pop('usel10n', True)
        bootstrap_version = kwargs.pop('bootstrap_version', 3)
        super(FechaWidget, self).__init__(usel10n=use10n, bootstrap_version=bootstrap_version, **kwargs)