from .clients import BaseClients
from .models import BaseModels
from .utils import BaseUtils

class MaleoCore:
    Clients = BaseClients
    Models = BaseModels
    Utils = BaseUtils