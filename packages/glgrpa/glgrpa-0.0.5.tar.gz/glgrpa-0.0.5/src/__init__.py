from .Terminal import Terminal
from .Windows import Windows
from .Chrome import Chrome
from .ARCA import ARCA

class GLGRPA: 
    def __init__(self, dev: bool = False, usuario: str = None, clave: str = None):
        self.dev = dev
        self.terminal = Terminal(dev=dev)
        self.windows = Windows(dev=dev)
        self.chrome = Chrome(dev=dev)
        self.arca = ARCA(dev=dev, usuario=usuario, clave=clave)