from models.partido_model import PartidoModel
from db.partido_repository import PartidoRepository

class PartidoController():
    
    def __init__(self):
        self.repo = PartidoRepository()
    
    def get(self): 
            return self.repo.get_all()

    def getById(self,id):
        return self.repo.get_by_id(id)
    
    def create(self,data):
        partido = PartidoModel(data) #creamos Mesa
        return {
            "id":self.repo.save(partido) #llamamos al repo en el metodo Save
        }
    def update(self, id,  data):
        partido = PartidoModel(data) #cremos mesa
        self.repo.update(id, partido)#llamamos update y pasamos los valores
    
    def delete(self,id):
        return self.repo.delete(id) #llamamos Delete y pasamos ID