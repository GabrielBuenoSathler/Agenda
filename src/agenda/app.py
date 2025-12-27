from fastapi import FastAPI, Depends
from .schema import (
    CidadeSchema,
    CidadePublic,
    UserPublic,
    UserSchema,
    Token ,

)

import  pandas as pd 
from fastapi.security import OAuth2PasswordRequestForm
from .geo import get_coordinates
from .models  import Cidade, User , Clima 
from sqlalchemy.orm import Session
from sqlalchemy import select 
from .database import get_session
from .meteo import temperature 
from fastapi import HTTPException
from .security import (
    get_current_user,
    get_password_hash,
    verify_password,
    create_access_token
)
from http import HTTPStatus
from .meteo import temperature 

app = FastAPI()


@app.get("/")
def root():
  return {"message": "Hello World"}

#@app.get("/lista_cidade" , responseModel=CidadePublic)
#def lista_cidade(Cidade: CidadeSchema, session: Session = Depends(get_session)):
#    pass
#
#
#


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)                                                               
def create_user(user: UserSchema, session: Session = Depends(get_session)):                                                                   
                                                                                                                                              
                                                                                                                                              
    db_user = session.scalar(                                                                                                                 
        select(User).where(                                                                                                                   
            (User.username == user.username) | (User.email == user.email)                                                                     
                                                                                                                                              
        )                                                                                                                                     
    )                                                                                                                                         
                                                                                                                                              
    if db_user:                                                                                                                               
        if db_user.username == user.username:                                                                                                 
                                                                                                                                              
                                                                                                                                              
            raise HTTPException(                                                                                                              
                status_code=HTTPStatus.CONFLICT,                                                                                              
                detail='Username already exists',                                                                                             
            )                                                                                                                                 
        elif db_user.email == user.email:                                                                                                     
            raise HTTPException(                                                                                                              
                status_code=HTTPStatus.CONFLICT,                                                                                              
                detail='Email already exists',                                                                                                
            )                                                                                                                                 
                                                                                                                                              
    db_user = User(                                                                                                                           
        username=user.username, password=get_password_hash(user.password), email=user.email                                                   
    )                                                                                                                                         
    session.add(db_user)                                                                                                                      
    session.commit()                                                                                                                          
    session.refresh(db_user)                                                                                                                  
                                                                                                                                              
    return db_user





def insert_temp_in_banco(dataframe,session : Session ):
    print(dataframe.dtypes)
    print(dataframe.info())
    temperatura = dataframe['temperature_2m'].tolist()
    data = dataframe['date'].tolist()
    for i in range(len(temperatura)):
        temp_obj = Clima(temperatura=float(temperatura[i]), data = data[i], id_cidade=1)
        session.add(temp_obj) 

    session.commit()

        
        


@app.post("/add_cidade" , response_model=CidadePublic)                             
def adiciona_cidade(cidade: CidadeSchema, session: Session = Depends(get_session),
                    current_user: User = Depends(get_current_user)):
    
    print(cidade)
    latitute,longitude  = get_coordinates(cidade.cidade_nome)
    clima_db = temperature(latitute, longitude)
    insert_temp_in_banco(clima_db,session) 
    db_cidade = Cidade(cidade_nome=cidade.cidade_nome, lat=latitute, long=longitude,user_id = current_user.id)
    session.add(db_cidade)                                                                                                  
    session.commit()                                                                                                      
    session.refresh(db_cidade)                                                                                              
    return db_cidade

@app.put("/up_cidade/{cidade_id}", response_model=CidadePublic)
def update_cidade(
    cidade_id: int,
    cidade: CidadeSchema,
    session: Session = Depends(get_session)
):
    db_cidade = session.get(Cidade, cidade_id)

    if not db_cidade:
        raise HTTPException(status_code=404, detail="Cidade não encontrada")

    db_cidade.cidade_nome = cidade.cidade_nome
    db_cidade.lat = cidade.lat
    db_cidade.long = cidade.long

    session.commit()
    session.refresh(db_cidade)

    return db_cidade


@app.delete("/del_cidade/{cidade_id}", response_model=CidadePublic)
def deleta_cidade(
    cidade_id: int,
    session: Session = Depends(get_session)
):
    db_cidade = session.get(Cidade, cidade_id)

    if not db_cidade:
        raise HTTPException(status_code=404, detail="Cidade não encontrada")

    session.delete(db_cidade)
    session.commit()

    return db_cidade


@app.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 


    session: Session = Depends(get_session),
):
    user = session.scalar(select(User).where(User.email == form_data.username)) 


    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password'
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password'
        )

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}

