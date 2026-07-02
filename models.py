from extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), default='organizador')
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)


class Evento(db.Model):
    __tablename__ = 'eventos'
    id = db.Column(db.Integer, primary_key=True)
    organizador_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    latitud = db.Column(db.Numeric(10, 7), nullable=False)
    longitud = db.Column(db.Numeric(10, 7), nullable=False)
    aforo = db.Column(db.Integer, default=0)
    qr_token = db.Column(db.String(64), unique=True, nullable=True)
    estado = db.Column(db.String(20), default='Borrador')  # Borrador, Publicado, EnCurso, Finalizado, Cancelado

    participantes = db.relationship('Participante', backref='evento', cascade='all, delete-orphan')
    agenda_items = db.relationship('AgendaItem', backref='evento', cascade='all, delete-orphan')


class Participante(db.Model):
    __tablename__ = 'participantes'
    id = db.Column(db.Integer, primary_key=True)
    evento_id = db.Column(db.Integer, db.ForeignKey('eventos.id'), nullable=False)
    nombre = db.Column(db.String(80), nullable=False)
    dni = db.Column(db.String(15), nullable=False)
    correo = db.Column(db.String(120), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    qr_code = db.Column(db.String(64), unique=True, nullable=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    asistencia = db.relationship('Asistencia', backref='participante', uselist=False, cascade='all, delete-orphan')


class Asistencia(db.Model):
    __tablename__ = 'asistencias'
    id = db.Column(db.Integer, primary_key=True)
    participante_id = db.Column(db.Integer, db.ForeignKey('participantes.id'), nullable=False)
    evento_id = db.Column(db.Integer, db.ForeignKey('eventos.id'), nullable=False)
    estado = db.Column(db.String(20), default='Pendiente')  # Pendiente, Confirmada, Ausente
    metodo = db.Column(db.String(10), nullable=True)  # QR, Manual
    fecha_marcado = db.Column(db.DateTime, nullable=True)


class AgendaItem(db.Model):
    __tablename__ = 'agenda'
    id = db.Column(db.Integer, primary_key=True)
    evento_id = db.Column(db.Integer, db.ForeignKey('eventos.id'), nullable=False)
    titulo = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    hora_inicio = db.Column(db.DateTime, nullable=False)
    hora_fin = db.Column(db.DateTime, nullable=False)
    responsable = db.Column(db.String(80), nullable=True)