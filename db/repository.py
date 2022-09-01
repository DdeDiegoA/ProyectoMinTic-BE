from typing import TypeVar, Generic,List,get_origin, get_args
from bson.objectid import ObjectId
from bson.dbref import DBRef
from bson import json_util
from db.db import Db
T=TypeVar('T')

class Repository(Generic[T]):
  def __init__(self):
    name = get_args(self.__orig_bases__[0] )[0].__name__.lower().replace('model','')
    self.db = Db()
    self.collection = self.db.collection(name)
  
  def get_all(self):
    results = self.collection.find()
    data = []
    for r in results:
      r["_id"] = r["_id"].__str__()
      r = self.transform_object_ids(r)
      r = self.get_values_db_ref(r)
      data.append(r)
    return data
  
  def query(self, filter): 
    results = self.collection.find(filter)
    data = []
    for r in results:
      r["_id"] = r["_id"].__str__()
      r = self.transform_object_ids(r)
      r = self.get_values_db_ref(r)
      data.append(r)
    return data
  
  def query_aggregation(self, filter):
    data = []
    for x in self.collection.aggregate(filter):
      x["_id"] = x["_id"].__str__()
      x = self.transform_object_ids(x)
      x = self.get_values_db_ref(x)
      data.append(x)
    return data
      
  def get_by_id(self, id):
    result = self.collection.find_one({"_id": ObjectId(id)})
    result["_id"] = result["_id"].__str__()
    result = self.transform_object_ids(result)
    result = self.get_values_db_ref(result)
    return result
  
  def save(self, item: T):
    item = self.transform_refs(item)
    id = ""
    if hasattr(item, '_id') and item._id != "":
      id = ObjectId(item._id)
      # delattr('_id', item.__dict__)
      self.collection.update_one({
        "_id": id
      }, {
        "$set": item.__dict__
      })
    else:
      result = self.collection.insert_one(item.__dict__)
      id = result.inserted_id
    return id.__str__()
  
  def update(self, id, item: T):
    id = ObjectId(id)
    # delattr('_id', item.__dict__)
    self.collection.update_one({
      "_id": id
    }, {
      "$set": item.__dict__
    })
      
      
  def delete(self, id):
    id = ObjectId(id)
    self.collection.delete_one({
        "_id": id
    })
      
  
  #Utility methods to transform the responses
  def transform_object_ids(self, x):
    for attribute in x.keys():
      if isinstance(x[attribute], ObjectId):
        x[attribute] = x[attribute].__str__()
      elif isinstance(x[attribute], list):
        x[attribute] = self.format_list(x[attribute])
      elif isinstance(x[attribute], dict):
        x[attribute]=self.transform_object_ids(x[attribute])
    return x
  
  def format_list(self, x):
    newList = []
    for item in x:
      if isinstance(item, ObjectId):
        newList.append(item.__str__())
    if len(newList) == 0:
      newList = x
    return newList
  
  def get_values_db_ref(self, x):
    keys = x.keys()
    for k in keys:
      if isinstance(x[k], DBRef):
        collection = self.db.collection(x[k].collection)
        valor = collection.find_one({"_id": ObjectId(x[k].id)})
        valor["_id"] = valor["_id"].__str__()
        x[k] = valor
        x[k] = self.get_values_db_ref(x[k])
      elif isinstance(x[k], list) and len(x[k]) > 0:
        x[k] = self.get_values_db_ref_from_list(x[k])
      elif isinstance(x[k], dict) :
        x[k] = self.get_values_db_ref(x[k])
    return x
  
  def get_values_db_ref_from_list(self, theList):
    newList = []
    for item in theList:
      value = self.collection.find_one({"_id": ObjectId(item.id)})
      value["_id"] = value["_id"].__str__()
      newList.append(value)
    return newList
   
  def transform_refs(self, item: T):
    theDict = item.__dict__
    keys = list(theDict.keys())
    for k in keys:
        if theDict[k].__str__().count("object") == 1:
          print(getattr(item, k))
          newObject = self.object_to_db_ref(getattr(item, k))
          setattr(item, k, newObject)
    return item

  def object_to_db_ref(self, item: T):
    nameCollection = item.__class__.__name__.lower().replace('model','')
    return DBRef(nameCollection, ObjectId(item._id))