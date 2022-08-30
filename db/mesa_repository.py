from db.repository import Repository
from models.mesa_model import MesaModel

class MesaRepository(Repository[MesaModel]):
    def __init__(self):
        super().__init__()