from flask import Blueprint, request, jsonify
from extensions import db
from models import Asistencia, Participante
from datetime import datetime

asistencias_bp = Blueprint('asistencias', __name__)

# Escanear QR para registrar asistencia (RF-14)
@asistencias_bp.route('/asistencias/escanear', methods=['POST'])
def escanear_qr():
    data = request.get_json()
    qr_code = data.get('qr_code')
    evento_id = data.get('evento_id')

    participante = Participante.query.filter_by(qr_code=qr_code, evento_id=evento_id).first()

    if not participante:
        return jsonify({"valido": False, "mensaje": "QR inválido o no pertenece a este evento"}), 404

    asistencia = Asistencia.query.filter_by(participante_id=participante.id, evento_id=evento_id).first()
    if not asistencia:
        asistencia = Asistencia(participante_id=participante.id, evento_id=evento_id)
        db.session.add(asistencia)

    asistencia.estado = 'Confirmada'
    asistencia.metodo = 'QR'
    asistencia.fecha_marcado = datetime.utcnow()
    db.session.commit()

    return jsonify({
        "valido": True,
        "mensaje": "Asistencia registrada",
        "participante": {
            "nombre": participante.nombre,
            "dni": participante.dni
        }
    })


# Marcar asistencia manualmente (RF-15)
@asistencias_bp.route('/asistencias/manual', methods=['POST'])
def marcar_manual():
    data = request.get_json()
    participante_id = data.get('participante_id')
    evento_id = data.get('evento_id')

    asistencia = Asistencia.query.filter_by(participante_id=participante_id, evento_id=evento_id).first()
    if not asistencia:
        asistencia = Asistencia(participante_id=participante_id, evento_id=evento_id)
        db.session.add(asistencia)

    asistencia.estado = 'Confirmada'
    asistencia.metodo = 'Manual'
    asistencia.fecha_marcado = datetime.utcnow()
    db.session.commit()

    return jsonify({"mensaje": "Asistencia marcada manualmente"})


# Reporte de asistencia de un evento (RF-16)
@asistencias_bp.route('/eventos/<int:evento_id>/reporte-asistencia', methods=['GET'])
def reporte_asistencia(evento_id):
    total_participantes = Participante.query.filter_by(evento_id=evento_id).count()
    confirmados = Asistencia.query.filter_by(evento_id=evento_id, estado='Confirmada').count()
    ausentes = Asistencia.query.filter_by(evento_id=evento_id, estado='Ausente').count()

    porcentaje = round((confirmados / total_participantes) * 100, 1) if total_participantes > 0 else 0

    return jsonify({
        "total_registrados": total_participantes,
        "asistentes_confirmados": confirmados,
        "ausentes": ausentes,
        "porcentaje_asistencia": porcentaje
    })