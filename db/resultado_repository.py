from db.repository import Repository
from models.resultado_model import ResultadoModel
from bson import ObjectId

class ResultadoRepository(Repository[ResultadoModel]):
    def __init__(self):
        super().__init__()
    
    def get_total(self): #obtener total de resultados
        data = self.get_all()
        result = {"results": {}}
        for register in data:
            if register["candidato"]["nombre"] + " " + register["candidato"]["apellido"] not in result["results"]:
                result["results"].update({register["candidato"]["nombre"] + " " + register["candidato"]["apellido"]:1})
            else:
                result["results"][register["candidato"]["nombre"] + " " + register["candidato"]["apellido"]] +=  1
        return result

    def total_candidato(self, candidato_id): # obtener el total de resultados por candidato
        filter = {"candidato.$id": ObjectId(candidato_id)}
        data = self.query(filter)
        result = {}
        for register in data:      
            if register["candidato"]["nombre"] + " " + register["candidato"]["apellido"] not in result:
                result.update({register["candidato"]["nombre"] + " " + register["candidato"]["apellido"]:1})
            else:
                result[register["candidato"]["nombre"] + " " + register["candidato"]["apellido"]] +=  1
        return result

    def aux(self, dict_aux, register):
        if register["candidato"]["nombre"] + " " + register["candidato"]["apellido"] not in dict_aux:
            dict_aux[register["candidato"]["nombre"] + " " + register["candidato"]["apellido"]]=1
        else:
            dict_aux[register["candidato"]["nombre"] + " " + register["candidato"]["apellido"]] +=1

        return dict_aux

    def get_total_mesa(self): #obtener total de resultados por mesas
        data = self.get_all()
        result = {}
        for register in data:
            if register["mesa"]["numero"] not in result:
                result[register["mesa"]["numero"]] = {register["candidato"]["nombre"] + " " + register["candidato"]["apellido"]:1}
                #result[register["mesa"]["numero"]].update({register["candidato"]["nombre"] + " " + register["candidato"]["apellido"]:1})
            else:
                dict_aux = result[register["mesa"]["numero"]]
                result[register["mesa"]["numero"]] = self.aux(dict_aux,register)
                #result["results"][register["candidato"]["nombre"] + " " + register["candidato"]["apellido"]] +=  1
        return result    


    def get_total_partido(self):
        data = self.get_all()
        result = {}
        for register in data:
            nom_partido = register["candidato"]["partido"]["nombre"]
            if nom_partido not in result:
                result[nom_partido] = {register["candidato"]["nombre"] + " " + register["candidato"]["apellido"]:1}
            else:
                dict_aux = result[nom_partido]
                result[nom_partido] = self.aux(dict_aux,register)
        return result
