from ast import Delete
from typing import TypeVar, Generic,List,get_origin, get_args
from bson.objectid import ObjectId
from bson.dbref import DBRef
from db.db import Db
T=TypeVar('T')

class Repository(Generic[T]): #Generic
    def __init__(self):
         name = get_args(self.__orig_bases__[0] )[0].__name__.lower().replace('model','') #con esto pasamos de llamarlo "Mesamodel" a "model"
         self.db = Db() #instanciamos base de datos
         self.collection = self.db.collection(name) #traemos la coleccion

    
#Metodos
    #Traer todos
    def get_all(self):
        results = self.collection.find() #traemos el objeto
        data = []
        for r in results: #recorremos el cursor en este caso
            r["_id"] = r["_id"].__str__() #los Ids a cadena de texto
            r = self.transform_object_ids(r)#transformamos en caso especifico
            r = self.get_values_db_ref(r)
            data.append(r)
        return data
    
    #Traer por ID
    def get_by_id(self, id): #recibe el ID
            result = self.collection.find_one({"_id": ObjectId(id)})#traemos el ObjectID
            result["_id"] = result["_id"].__str__()
            result = self.transform_object_ids(result)
            result = self.get_values_db_ref(result)
            return result
    
    #Guardar
    def save(self, item: T): #recibe un item del mismo tipo indicado en el generico (T)
        item = self.transform_refs(item) #si posee relacion compuesta la transformamos
        if hasattr(item, '_id') and item._id != "": #si pasa un ID lo actualizamos, sí no lo creamos.
            id= ObjectId(item._id)#la transformamos en ObjID
            # delattr('_id', item.__dict__) #removemos el OBjID para no actualizarlo
            self.collection.update_one({ #actualizar uno
                "_id": id #con el ID
            },{
                "$set": item.__dict__ #ese Item
            })  
        else: #en caso de crearlo
            result = self.collection.insert_one(item.__dict__)
            id = result.inserted_id.__str__()
        return id.__str__() #retornamos el ID creado
    
    #Actualizar
    def update (self, id, item: T):
        id = ObjectId(id)
        # delattr('_id', item.__dict__) #removemos el OBjID para no actualizarlo
        self.collection.update_one({ 
                "_id": id #con el ID
            }, {
                "$set": item.__dict__  #ese Item
            })
        
    #Borrar   
    def delete (self, id):
        id = ObjectId(id)
        self.collection.delete_one({ #borrar uno recibe un filtro
            "_id": id
        })
                
    def query(self, filter): 
        results = self.collection.find(filter)
        data = []
        for r in results:
            r["_id"] = r["_id"].__str__()
            r = self.transform_object_ids(r)
            r = self.get_values_db_ref(r)
            data.append(r)
        return data
    
    
    #metodos de transformacion de respuestas
    
    def transform_object_ids(self, x):
        for attribute in x.keys():
            if isinstance(x[attribute], ObjectId): #en caso de ser un ObjectID
                x[attribute] = x[attribute].__str__()
            elif isinstance(x[attribute],list): #en caso de ser una lista
                x[attribute]= self.formatList(x[attribute])
            elif isinstance(x[attribute], dict): #en caso de ser diccionario
                x[attribute]= self.transform_object_ids(x[attribute])
            return x
        
        #formatear list
    def format_list(self, x):
        newList = []
        for item in x:
            if isinstance(item, ObjectId):
                newList.append(item.__str__())
            if len(newList) == 0:
             newList = x
            return newList
        
        #cuando encuentro ID que referencia otros valores
    def get_values_db_ref(self, x):
        keys = x.keys()
        for k in keys:
            if isinstance(x[k], DBRef):
                collection = self.db.collection(x[k].collection)
                valor = collection.find_one({"_id": ObjectId(x[k].id)}) #para retornar el Object
                valor["_id"] = valor["_id"].__str__()
                x[k] = valor
                x[k] = self.get_values_db_ref(x[k])
            elif isinstance(x[k], list) and len(x[k]) > 0:
                x[k] = self.get_values_db_ref_from_list(x[k])
            elif isinstance(x[k], dict) :
                x[k] = self.get_values_db_ref(x[k])
            return x
        
        #Traer valores de ref como lista
    def get_values_db_ref_from_list(self, theList):
        newList = []
        for item in theList:
            value = self.collection.find_one({"_id": ObjectId(item.id)})
            value["_id"] = value["_id"].__str__()
            newList.append(value)
        return newList
    
        #trabsfornar referencia
    def transform_refs(self, item: T):
        theDict = item.__dict__
        keys = list(theDict.keys()) #accedemos a las llaves del diccionario
        for k in keys:
            if theDict[k].__str__().count("object") == 1: #sí algun tipo del dicc es OBJ
                newObject = self.object_to_db_ref(getattr(item, k)) #llamamos al MEtodo
                setattr(item, k, newObject)
        return item

    def object_to_db_ref(self, item: T):
        nameCollection = item.__class__.__name__.lower().replace('model','')
        return DBRef(nameCollection, ObjectId(item._id)) #crea referencia del obj con el ID