
from datetime import datetime
from sqlalchemy.orm import (
    Mapped, mapped_as_dataclass, registry, mapped_column, relationship
)
from sqlalchemy import func, ForeignKey
from sqlalchemy import DateTime

table_registry = registry()


@mapped_as_dataclass(table_registry)
class User:
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    Evento: Mapped[list['Evento']] = relationship(
        init=False,
        cascade='all, delete-orphan',
        lazy='selectin',
    )
    Cidade: Mapped[list['Cidade']] = relationship(  
         init=False,                                 
         cascade='all, delete-orphan',               
         lazy='selectin',                            
     )                                               

    
@mapped_as_dataclass(table_registry)
class Evento:
    __tablename__ = "Evento"

    id_evento: Mapped[int] = mapped_column(init=False, primary_key=True)

    # Foreign key: cada Book pertence a UM User
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    nome_da_tarefa: Mapped[str]
    data_tarefa: Mapped[datetime]
    data_limite: Mapped[datetime]
    lugar: Mapped[str]
    problema: Mapped[datetime] 
    solucao: Mapped[str]  


    
@mapped_as_dataclass(table_registry)                                       
class Cidade:                                                              
    __tablename__ = "Cidade" 
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False) 
    id_cidade : Mapped[int] = mapped_column (init = False , primary_key=True)
    cidade_nome : Mapped[str]  
    lat : Mapped[float]
    long : Mapped[float]
    Clima: Mapped[list['Clima']] = relationship(   
         init=False,                                 
         cascade='all, delete-orphan',               
         lazy='selectin',                            
     )                                               




@mapped_as_dataclass(table_registry)
class Clima:
    __tablename__ = "Clima"
    id_clima : Mapped[int] = mapped_column (init = False , primary_key=True)
    id_cidade: Mapped[int] = mapped_column(ForeignKey("Cidade.id_cidade"), nullable=False)
    data : Mapped[datetime]
    temperatura: Mapped[float]


    
                                                                           
                                                                           







