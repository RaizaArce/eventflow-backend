from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, jwt

app = Flask(__name__)
app.config.from_object(Config)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

db.init_app(app)
jwt.init_app(app)
CORS(app)

from routes.auth import auth_bp
app.register_blueprint(auth_bp)

from routes.eventos import eventos_bp
app.register_blueprint(eventos_bp)

from routes.participantes import participantes_bp
app.register_blueprint(participantes_bp)

from routes.asistencias import asistencias_bp
app.register_blueprint(asistencias_bp)

from routes.agenda import agenda_bp
app.register_blueprint(agenda_bp)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return {"mensaje": "EventFlow API funcionando"}

if __name__ == '__main__':
    app.run(debug=True)