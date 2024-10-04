# File path: app/models/contact_model.py

from extensions import db
from app.models.address_model import Address

class Contact(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=True)  # Cambiado a nullable=True
    telefono = db.Column(db.String(15), nullable=False, unique=True)
    direccion = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True)

    # Relación de uno a muchos con Address
    addresses = db.relationship("Address", back_populates="contact", cascade="all, delete-orphan")
