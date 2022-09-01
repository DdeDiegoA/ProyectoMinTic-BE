from models.mesa_model import MesaModel
from db.mesa_repository import MesaRepository

class MesaController():
    
    def __init__(self):
        self.repo = MesaRepository()
    
    def get(self): 
        return self.repo.get_all()

    def getById(self,id):
        return self.repo.get_by_id(id)
    
    def create(self,data):
        mesa = MesaModel(data) #creamos Mesa
        return {
            "id":self.repo.save(mesa) #llamamos al repo en el metodo Save
        }
    def update(self, id,  data):
        mesa = MesaModel(data) #cremos mesa
        self.repo.update(id, mesa)#llamamos update y pasamos los valores
    
    def delete(self,id):
        return self.repo.delete(id) #llamamos Delete y pasamos ID
        