from flask import Blueprint, request, jsonify
from extensions import db
from models import AgendaItem
from datetime import datetime

agenda_bp = Blueprint('agenda', __name__)

# Listar agenda de un evento, ordenada cronológicamente (RF-20)
@agenda_bp.route('/eventos/<int:evento_id>/agenda', methods=['GET'])
def listar_agenda(evento_id):
    items = AgendaItem.query.filter_by(evento_id=evento_id).order_by(AgendaItem.hora_inicio).all()
    resultado = []
    for item in items:
        resultado.append({
            "id": item.id,
            "titulo": item.titulo,
            "descripcion": item.descripcion,
            "hora_inicio": item.hora_inicio.isoformat(),
            "hora_fin": item.hora_fin.isoformat(),
            "responsable": item.responsable
        })
    return jsonify(resultado)


# Crear actividad de agenda (RF-17)
@agenda_bp.route('/eventos/<int:evento_id>/agenda', methods=['POST'])
def crear_actividad(evento_id):
    data = request.get_json()
    nueva_actividad = AgendaItem(
        evento_id=evento_id,
        titulo=data['titulo'],
        descripcion=data.get('descripcion', ''),
        hora_inicio=datetime.fromisoformat(data['hora_inicio']),
        hora_fin=datetime.fromisoformat(data['hora_fin']),
        responsable=data.get('responsable')
    )
    db.session.add(nueva_actividad)
    db.session.commit()
    return jsonify({"mensaje": "Actividad creada", "id": nueva_actividad.id}), 201


# Editar actividad de agenda (RF-18)
@agenda_bp.route('/agenda/<int:actividad_id>', methods=['PUT'])
def editar_actividad(actividad_id):
    item = AgendaItem.query.get_or_404(actividad_id)
    data = request.get_json()
    item.titulo = data.get('titulo', item.titulo)
    item.descripcion = data.get('descripcion', item.descripcion)
    if 'hora_inicio' in data:
        item.hora_inicio = datetime.fromisoformat(data['hora_inicio'])
    if 'hora_fin' in data:
        item.hora_fin = datetime.fromisoformat(data['hora_fin'])
    item.responsable = data.get('responsable', item.responsable)
    db.session.commit()
    return jsonify({"mensaje": "Actividad actualizada"})


# Eliminar actividad de agenda (RF-19)
@agenda_bp.route('/agenda/<int:actividad_id>', methods=['DELETE'])
def eliminar_actividad(actividad_id):
    item = AgendaItem.query.get_or_404(actividad_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"mensaje": "Actividad eliminada"})