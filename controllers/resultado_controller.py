from models.resultado_model import ResultadoModel
from models.mesa_model import MesaModel
from models.candidato_model import CandidatoModel

from db.resultado_repository import ResultadoRepository
from db.mesa_repository import MesaRepository 
from db.candidato_repository import CandidatoRepository

class ResultadoController():
    
    def __init__(self):
        self.repo = ResultadoRepository()
        self.repo_mesa = MesaRepository()
        self.repo_candidato = CandidatoRepository()
    
    def get(self): 
            return self.repo.get_all()

    def getById(self,id):
        return self.repo.get_by_id(id)
        
    def create(self, data, mesa_id, candidato_id):
        resultado = ResultadoModel(data) #creamos Resultado
        mesa = self.repo_mesa.get_by_id(mesa_id)
        resultado.mesa = MesaModel(mesa)

        candidato = self.repo_candidato.get_by_id(candidato_id)
        resultado.candidato = CandidatoModel(candidato)
        
        return {
            "id":self.repo.save(resultado) #llamamos al repo en el metodo Save
        }
    def update(self, id,  data):
        resultado = ResultadoModel(data) #cremos Resultado
        self.repo.update(id, resultado)#llamamos update y pasamos los valores
    
    def delete(self,id):
        return self.repo.delete(id) #llamamos Delete y pasamos ID