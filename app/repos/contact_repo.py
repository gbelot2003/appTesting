# File path: app/repos/contact_repo.py

from sqlalchemy.orm import Session
from app.models.contact_model import Contact as Contacto
from app.models.address_model import Address
from extensions import db  # Asumimos que `db` es la instancia de SQLAlchemy o la sesión global

class ContactRepo:
    @staticmethod
    def crear_contacto(db_session: Session, telefono, nombre=None, direccion=None, email=None):
        nuevo_contacto = Contacto(nombre=nombre, telefono=telefono, direccion=direccion, email=email)
        db_session.add(nuevo_contacto)
        db_session.commit()
        return nuevo_contacto

    @staticmethod
    def obtener_contacto_por_telefono(db_session: Session, telefono):
        return db_session.query(Contacto).filter_by(telefono=telefono).first()

    @staticmethod
    def obtener_todos_contactos(db_session: Session):
        return db_session.query(Contacto).all()

    @staticmethod
    def actualizar_contacto(db_session: Session, contacto_id, nombre=None, telefono=None, direccion=None, email=None):
        contacto = db_session.query(Contacto).filter_by(id=contacto_id).first()
        if contacto:
            if nombre:
                contacto.nombre = nombre
            if telefono:
                contacto.telefono = telefono
            if direccion:
                contacto.direccion = direccion
            if email:
                contacto.email = email
            db_session.commit()
        return contacto

    @staticmethod
    def eliminar_contacto(db_session: Session, contacto_id):
        contacto = db_session.query(Contacto).filter_by(id=contacto_id).first()
        if contacto:
            db_session.delete(contacto)
            db_session.commit()
        return contacto

    @staticmethod
    def agregar_direccion(db_session: Session, direccion: Address):
        """
        Agrega una nueva dirección asociada a un contacto en la base de datos.
        """
        db_session.add(direccion)
        db_session.commit()
        db_session.refresh(direccion)
        return direccion

    @staticmethod
    def actualizar_direccion(db_session: Session, contact_id: int, direccion: str):
        """
        Actualiza la dirección principal del contacto con el ID proporcionado.
        """
        contacto = db_session.query(Contacto).filter(Contacto.id == contact_id).first()
        if contacto:
            contacto.direccion = direccion
            db_session.commit()
            db_session.refresh(contacto)
        return contacto
