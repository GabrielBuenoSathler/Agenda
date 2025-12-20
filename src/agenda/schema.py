from pydantic  import BaseModel , EmailStr
from datetime import date, datetime, time, timedelta
class UserPublic(BaseModel):
    id : int 
    cidade : str
    username : str
    email : EmailStr
    password : str
    lat : float
    long : float 


class UserSchema(BaseModel):
    email : str
    username : str


class EventoPublic(BaseModel):
    usuario_id : int 
    id_evento : int 
    nome_evento : str
    problema : str 
    data_de_criacao : datetime
    data_limite : datetime 
    lugar : str
    usuario_atendimento : str  
    solucao : str 

class CidadeSchema(BaseModel): 
    cidade_nome : str
    lat : float
    long : float 
      

class CidadePublic(BaseModel):
    id_cidade : int 
    cidade_nome : str
    long : float
    lat : float 

class EventoSchema(BaseModel): 
    problema : str
    data_de_criacao : datetime      
    data_limite : datetime          
    lugar : str                     
    usuario_atendimento : str       
    solucao : str                   
