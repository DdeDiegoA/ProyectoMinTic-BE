from models.candidato_model import CandidatoModel
from models.partido_model import PartidoModel

from db.candidato_repository import CandidatoRepository
from db.partido_repository import PartidoRepository

class CandidatoController():
    
    def __init__(self):
        self.repo = CandidatoRepository()
        self.repo_partido = PartidoRepository()
    
    def get(self, args): 
            return self.repo.get_all()

    '''
    def get(self, args):
        params = args.to_dict()
        filter = {}
    
        if 'university' in params:
            if not '$and' in filter:
                filter['$and'] = []
            filter['$and'].append({
                'university': {
                '$regex': f"^{params['university']}",
                '$options': 'i'
                }
            })
        
        if 'age' in params:
            if not '$and' in filter:
                filter['$and'] = []
            filter['$and'].append({
                'age': {
                '$gte': int(params['age'])
                }
            })
            if len(filter.keys()) == 0:
                return self.repo.get_all()
            return self.repo.query(filter)'''


    def getById(self,id):
        return self.repo.get_by_id(id)
    
    '''
    def create(self,data):
        candidato = CandidatoModel(data) #creamos Mesa
        return {
            "id":self.repo.save(candidato) #llamamos al repo en el metodo Save
        }
    '''


    def create(self, data, partido_id):
        candidato = CandidatoModel(data) #creamos Mesa
        partido = self.repo_partido.get_by_id(partido_id)
        candidato.partido = PartidoModel(partido)
        
        return {
            "id":self.repo.save(candidato) #llamamos al repo en el metodo Save
        }
        
    def update(self, id,  data):
        candidato = CandidatoModel(data) #cremos mesa
        self.repo.update(id, candidato)#llamamos update y pasamos los valores
    
    def delete(self,id):
        return self.repo.delete(id) #llamamos Delete y pasamos ID