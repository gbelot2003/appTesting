# File path: app/models/address_model.py

from extensions import db

class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)  # ForeignKey to Contact
    type = db.Column(db.String(50), nullable=False)  # Tipo de dirección: 'pickup', 'delivery', 'principal', etc.
    address_line = db.Column(db.String(255), nullable=False)  # Dirección completa
    latitude = db.Column(db.Float, nullable=True)  # Latitud de la dirección
    longitude = db.Column(db.Float, nullable=True)  # Longitud de la dirección
    is_primary = db.Column(db.Boolean, default=False)  # Indica si es la dirección principal

    # Relación con el modelo Contact
    contact = db.relationship("Contact", back_populates="addresses")

