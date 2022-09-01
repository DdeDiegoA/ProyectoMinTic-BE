from db.repository import Repository
from models.candidato_model import CandidatoModel

class CandidatoRepository(Repository[CandidatoModel]):
    def __init__(self):
        super().__init__()