from db.repository import Repository
from models.resultado_model import ResultadoModel

class ResultadoRepository(Repository[ResultadoModel]):
    def __init__(self):
        super().__init__()