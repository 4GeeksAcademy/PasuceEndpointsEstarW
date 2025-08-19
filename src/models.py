from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean,Table,Column,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship

db = SQLAlchemy()


favoritos_personaje = Table(
    "favoritos _personaje",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("personaje_id", ForeignKey("personaje.id"), primary_key=True),
)

favoritos_planeta = Table(
    "favoritos _planeta",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("planeta_id", ForeignKey("planeta.id"), primary_key=True),
)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False) 
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    fav_personajes: Mapped[List["Personaje"]] = relationship(secondary=favoritos_personaje)
    
    fav_planetas: Mapped[List["Planeta"]] = relationship(secondary=favoritos_planeta)
  


    def serialize(self):
        return {
            "id": self.id,
            "user_name" :self.user_name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class Personaje(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False) 
    race: Mapped[str] = mapped_column(String(120),  nullable=False)
    image: Mapped[str] = mapped_column(String(152), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name" :self.name,
            "race": self.race,
            "image":self.image

        }
    

class Planeta(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False) 
    galaxy: Mapped[str] = mapped_column(String(120),  nullable=False)
    image: Mapped[str] = mapped_column(String(152), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name" :self.name,
            "galaxy": self.galaxy,
            "image":self.image

        }   