from flask import Blueprint, request, jsonify
from extensions import db
from models import Evento
from datetime import datetime
import uuid

eventos_bp = Blueprint('eventos', __name__)

# Listar todos los eventos (RF-07)
@eventos_bp.route('/eventos', methods=['GET'])
def listar_eventos():
    eventos = Evento.query.all()
    resultado = []
    for e in eventos:
        resultado.append({
            "id": e.id,
            "nombre": e.nombre,
            "descripcion": e.descripcion,
            "fecha_inicio": e.fecha_inicio.isoformat(),
            "fecha_fin": e.fecha_fin.isoformat(),
            "direccion": e.direccion,
            "latitud": float(e.latitud),
            "longitud": float(e.longitud),
            "aforo": e.aforo,
            "estado": e.estado
        })
    return jsonify(resultado)


# Crear un evento (RF-04)
@eventos_bp.route('/eventos', methods=['POST'])
def crear_evento():
    data = request.get_json()
    nuevo_evento = Evento(
        organizador_id=data['organizador_id'],
        nombre=data['nombre'],
        descripcion=data.get('descripcion', ''),
        fecha_inicio=datetime.fromisoformat(data['fecha_inicio']),
        fecha_fin=datetime.fromisoformat(data['fecha_fin']),
        direccion=data['direccion'],
        latitud=data['latitud'],
        longitud=data['longitud'],
        aforo=data.get('aforo', 0),
        qr_token=str(uuid.uuid4()),
        estado='Borrador'
    )
    db.session.add(nuevo_evento)
    db.session.commit()
    return jsonify({"mensaje": "Evento creado", "id": nuevo_evento.id}), 201


# Ver el detalle de un evento (RF-08)
@eventos_bp.route('/eventos/<int:evento_id>', methods=['GET'])
def detalle_evento(evento_id):
    e = Evento.query.get_or_404(evento_id)
    return jsonify({
        "id": e.id,
        "nombre": e.nombre,
        "descripcion": e.descripcion,
        "fecha_inicio": e.fecha_inicio.isoformat(),
        "fecha_fin": e.fecha_fin.isoformat(),
        "direccion": e.direccion,
        "latitud": float(e.latitud),
        "longitud": float(e.longitud),
        "aforo": e.aforo,
        "estado": e.estado,
        "cantidad_participantes": len(e.participantes),
        "cantidad_actividades_agenda": len(e.agenda_items)
    })


# Editar un evento (RF-05)
@eventos_bp.route('/eventos/<int:evento_id>', methods=['PUT'])
def editar_evento(evento_id):
    e = Evento.query.get_or_404(evento_id)
    data = request.get_json()
    e.nombre = data.get('nombre', e.nombre)
    e.descripcion = data.get('descripcion', e.descripcion)
    if 'fecha_inicio' in data:
        e.fecha_inicio = datetime.fromisoformat(data['fecha_inicio'])
    if 'fecha_fin' in data:
        e.fecha_fin = datetime.fromisoformat(data['fecha_fin'])
    e.direccion = data.get('direccion', e.direccion)
    e.aforo = data.get('aforo', e.aforo)
    e.estado = data.get('estado', e.estado)
    db.session.commit()
    return jsonify({"mensaje": "Evento actualizado"})


# Eliminar un evento (RF-06)
@eventos_bp.route('/eventos/<int:evento_id>', methods=['DELETE'])
def eliminar_evento(evento_id):
    e = Evento.query.get_or_404(evento_id)
    db.session.delete(e)
    db.session.commit()
    return jsonify({"mensaje": "Evento eliminado"})