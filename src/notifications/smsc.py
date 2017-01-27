import requests
from urllib.parse import quote_plus
from django.conf import settings

BASE_URL = "https://www.smsc.com.ar/api/0.2/?alias={alias}&apikey={apikey}"


class SmscResponse:
    """
    This class contain the information given for response from service.

    All public methods returns an object of this type
    From wiki:
    Datos devueltos

    Te devolverá información en formato JSON. Los 3 valores serán:
    code: Código de estado de la operación (OK, Error, etc)
    message: Mensaje del código devuelto.
    data: Si la operación fue de consulta, aquí estará la información devuelta.
    """
    def __init__(self, data):
        self.code = data["code"]
        self.message = data["message"]
        self.data = data["data"]

    def __str__(self):
        if self.message:
            return "[{}] {}".format(self.code, self.message)
        return "[{}] {}".format(self.code, self.data)


class SmscApi:
    """
    Main class that expose public methods from Api SMSC.

    """
    def _get_base_url(self):
        try:
            return BASE_URL.format(alias=settings.SMSC_ALIAS, apikey=settings.SMSC_APIKEY)
        except KeyError:
            raise Exception("Please, setup SMSC settings correctly.")

    def send_sms(self, number, message, time=None):
        """
        Send a sms message to given number via smsc service.

        From wiki:

        cmd=enviar
            O no especificar.
        num=2627-000000
            Se puede especificar sin guión (-), aunque no es recomendable.
        msj=HolaMundo!
            El mensaje que será enviado. Ten en cuenta que los mensajes con más de 160 caracteres consumirán más
            crédito, al igual que los que poseen caracteres como las vocales con acento.
        time= [opcional]
            Fecha y Hora en formato YYYY-MM-DD HH:MM:SS (ej: "2013-01-31 22::44:50") o en UNIX_TIMESTAMP (GMT+0).
        """
        url = "{}&cmd=enviar&num={}&msj={}".format(self._get_base_url(), number, quote_plus(message))
        if time:
            url += "&time="
            try:
                url += time.strftime("%Y-%m-%d %H:%M:%S")
            except AttributeError:
                url += time

        response = requests.get(url)
        r = SmscResponse(response.json())
        return r

    def get_latest_sent_sms(self, ultimoid=0):
        """
        From wiki:
        :
        Consulta de Enviados
        cmd=enviados
        ultimoid=0
        Opcional. Puede espedificar el último ID de mensaje que consultó, para ahorrar ancho de banda
        y aumentar la velocidad de respuesta. Si coloca 0, recibirá los últimos 50 SMSC enviados.
        """
        url = "{}&cmd=enviados&ultimoid={}".format(self._get_base_url(), ultimoid)
        response = requests.get(url)
        r = SmscResponse(response.json())
        return r

    def get_latest_received_sms(self, ultimoid=0):
        """
        From wiki:
        Consulta de Recibidos
        cmd=recibidos
        ultimoid=0
        Opcional. Puede espedificar el último ID de mensaje que consultó, para ahorrar ancho de banda y
        aumentar la velocidad de respuesta. Si coloca 0, recibirá los últimos 50 SMSC recibidos.
        """
        url = "{}&cmd=recibidos&ultimoid={}".format(self._get_base_url(), ultimoid)
        response = requests.get(url)
        r = SmscResponse(response.json())
        return r

    def get_status_service(self):
        """
        From wiki:
        Consultar estado del servicio
        cmd=estado
        """
        response = requests.get("{}&cmd=estado".format(self._get_base_url()))
        r = SmscResponse(response.json())
        return r

    def get_credit(self):
        """
        From wiki:
        Consultar saldo
        cmd=saldo
        """
        response = requests.get("{}&cmd=saldo".format(self._get_base_url()))
        r = SmscResponse(response.json())
        return r
