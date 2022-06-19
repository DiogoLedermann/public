
class Barril:

    def __init__(self) -> None:
        self.id = None
        self.bebida = None
        self.litros = None
        self.status = None

class Maquina:

    def __init__(self) -> None:
        self.id = None
        self.status = None

class Cilindro:

    def __init__(self) -> None:
        self.id = None
        self.status = None

class Estoque:

    def __init__(self) -> None:
        self.barris = []
        self.maquinas = []
        self.cilindros = []

class EmUso:

    def __init__(self) -> None:
        self.barris = []
        self.maquinas = []
        self.cilindros = []

class Avariados:

    def __init__(self) -> None:
        self.barris = []
        self.maquinas = []
        self.cilindros = []
