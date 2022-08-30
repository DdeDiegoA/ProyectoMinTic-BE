from models.mesa_model import MesaModel
from db.mesa_repository import MesaRepository

class MesaController():
    
    def __init__(self):
        self.repo = MesaRepository()
    
    def get(self):
        return self.repo.get_all()
    
    def getById(self,id):
        return self.repo.get_by_id(id)
    
    # def create(data):
    #     mesa.append(
    #         MesaModel(data)
    #     )
    #     return mesa[data.id]
    # def update(id, data):
    #     mesa= mesa[id]
    #     for key,value in data.items():
    #         mesa[key] = value
    
    # def delete(id):
    #     del mesa[id]
        