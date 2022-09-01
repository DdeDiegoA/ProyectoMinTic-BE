from models.resultado_model import ResultadoModel
from db.resultado_repository import ResultadoRepository

class ResultadoController():
    
    def __init__(self):
        self.repo = ResultadoRepository()
    
    def get(self): 
            return self.repo.get_all()

    def getById(self,id):
        return self.repo.get_by_id(id)
    
    def create(self,data):
        resultado = ResultadoModel(data) #creamos resultado
        return {
            "id":self.repo.save(resultado) #llamamos al repo en el metodo Save
        }
    def update(self, id,  data):
        resultado = ResultadoModel(data) #cremos mesa
        self.repo.update(id, resultado)#llamamos update y pasamos los valores
    
    def delete(self,id):
        return self.repo.delete(id) #llamamos Delete y pasamos ID