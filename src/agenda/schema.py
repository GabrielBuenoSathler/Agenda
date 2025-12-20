from pydantic  import BaseModel , EmailStr
import datetime 

class UserPublic(BaseModel):
    id : int 
    cidade : str
    username : str
    email : EmailStr
    password : str 


class UserSchema(BaseModel):
    email : str
    username : str
    cidade : str


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


class EventoSchema(BaseModel): 
    problema : str
    data_de_criacao : datetime      
    data_limite : datetime          
    lugar : str                     
    usuario_atendimento : str       
    solucao : str                   
