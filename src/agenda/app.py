from fastapi import FastAPI, Depends
from .schema import (
    CidadeSchema,
    CidadePublic

)
from .geo import get_coordinates
from .models  import Cidade
from sqlalchemy.orm import Session
from .database import get_session 

app = FastAPI()


@app.get("/")
def root():
  return {"message": "Hello World"}

#@app.get("/lista_cidade" , responseModel=CidadePublic)
#def lista_cidade(Cidade: CidadeSchema, session: Session = Depends(get_session)):
#    pass

@app.post("/add_cidade" , response_model=CidadePublic)                             
def adiciona_cidade(cidade: CidadeSchema, session: Session = Depends(get_session)):   
    
    db_cidade = Cidade(cidade_nome =cidade.cidade_nome,lat = cidade.lat, long = cidade.long)                                                                                                                  
    session.add(db_cidade)                                                                                                  
    session.commit()                                                                                                      
    session.refresh(db_cidade)                                                                                              
    return db_cidade

@app.put("/up_cidade" , response_model=CidadePublic)                           
def update_cidade(Cidade: CidadeSchema, session: Session = Depends(get_session)):
    pass                                                                        
                                                                                
@app.delete("/del_cidade" , response_model=CidadePublic)                           
def deleta_cidade(Cidade: CidadeSchema, session: Session = Depends(get_session)):
    pass                                                                        
                                                                                



