from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models import Participante
import uuid

participantes_bp = Blueprint('participantes', __name__)

@participantes_bp.route('/eventos/<int:evento_id>/participantes', methods=['GET'])
@jwt_required()
def listar_participantes(evento_id):
    participantes = Participante.query.filter_by(evento_id=evento_id).all()
    resultado = []
    for p in participantes:
        estado_asistencia = p.asistencia.estado if p.asistencia else "Sin registrar"
        resultado.append({
            "id": p.id,
            "nombre": p.nombre,
            "dni": p.dni,
            "correo": p.correo,
            "telefono": p.telefono,
            "qr_code": p.qr_code,
            "estado_asistencia": estado_asistencia
        })
    return jsonify(resultado)


@participantes_bp.route('/eventos/<int:evento_id>/participantes', methods=['POST'])
@jwt_required()
def registrar_participante(evento_id):
    data = request.get_json()
    nuevo_participante = Participante(
        evento_id=evento_id,
        nombre=data['nombre'],
        dni=data['dni'],
        correo=data.get('correo'),
        telefono=data.get('telefono'),
        qr_code=str(uuid.uuid4())
    )
    db.session.add(nuevo_participante)
    db.session.commit()
    return jsonify({
        "mensaje": "Participante registrado",
        "id": nuevo_participante.id,
        "qr_code": nuevo_participante.qr_code
    }), 201


@participantes_bp.route('/participantes/<int:participante_id>', methods=['PUT'])
@jwt_required()
def editar_participante(participante_id):
    p = Participante.query.get_or_404(participante_id)
    data = request.get_json()
    p.nombre = data.get('nombre', p.nombre)
    p.dni = data.get('dni', p.dni)
    p.correo = data.get('correo', p.correo)
    p.telefono = data.get('telefono', p.telefono)
    db.session.commit()
    return jsonify({"mensaje": "Participante actualizado"})


@participantes_bp.route('/participantes/<int:participante_id>', methods=['DELETE'])
@jwt_required()
def eliminar_participante(participante_id):
    p = Participante.query.get_or_404(participante_id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({"mensaje": "Participante eliminado"})