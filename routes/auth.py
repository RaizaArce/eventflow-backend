from flask import Blueprint, request, jsonify
from extensions import db
from models import User
import bcrypt
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/registro', methods=['POST'])
def registro():
    data = request.get_json()
    hashed = bcrypt.hashpw(data['contrasena'].encode(), bcrypt.gensalt())
    nuevo_usuario = User(
        nombre=data['nombre'],
        correo=data['correo'],
        contrasena=hashed.decode()
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({"mensaje": "Usuario creado"}), 201

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = User.query.filter_by(correo=data['correo']).first()
    if usuario and bcrypt.checkpw(data['contrasena'].encode(), usuario.contrasena.encode()):
        token = create_access_token(identity=str(usuario.id))
        return jsonify({"token": token, "nombre": usuario.nombre, "rol": usuario.rol})
    return jsonify({"error": "Credenciales inválidas"}), 401