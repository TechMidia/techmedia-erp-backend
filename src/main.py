import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.models.cliente import Cliente
from src.models.servico import Servico
from src.models.pedido import Pedido
from src.models.financeiro import Financeiro
from src.models.social_media import SocialMedia
from src.models.design import Design
from src.models.grafica import Grafica
from src.models.fornecedor import Fornecedor
from src.models.tarefa import Tarefa
from src.models.automacao import Automacao

from src.routes.user import user_bp
from src.routes.cliente import cliente_bp
from src.routes.servico import servico_bp
from src.routes.pedido import pedido_bp
from src.routes.financeiro import financeiro_bp
from src.routes.social_media import social_media_bp
from src.routes.design import design_bp
from src.routes.grafica import grafica_bp
from src.routes.fornecedor import fornecedor_bp
from src.routes.tarefa import tarefa_bp
from src.routes.automacao import automacao_bp
from src.routes.dashboard import dashboard_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app)

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(cliente_bp, url_prefix='/api')
app.register_blueprint(servico_bp, url_prefix='/api')
app.register_blueprint(pedido_bp, url_prefix='/api')
app.register_blueprint(financeiro_bp, url_prefix='/api')
app.register_blueprint(social_media_bp, url_prefix='/api')
app.register_blueprint(design_bp, url_prefix='/api')
app.register_blueprint(grafica_bp, url_prefix='/api')
app.register_blueprint(fornecedor_bp, url_prefix='/api')
app.register_blueprint(tarefa_bp, url_prefix='/api')
app.register_blueprint(automacao_bp, url_prefix='/api')
app.register_blueprint(dashboard_bp, url_prefix='/api')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()
    
    # Create default users if they don't exist
    from src.models.user import User
    from werkzeug.security import generate_password_hash
    
    if not User.query.filter_by(username='laina_carmo').first():
        admin1 = User(
            username='laina_carmo',
            email='laina@techmedia.com',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin1)
    
    if not User.query.filter_by(username='yuri_carmo').first():
        admin2 = User(
            username='yuri_carmo',
            email='yuri@techmedia.com',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin2)
    
    if not User.query.filter_by(username='alysson_designer').first():
        designer = User(
            username='alysson_designer',
            email='alysson@techmedia.com',
            password_hash=generate_password_hash('designer123'),
            role='designer'
        )
        db.session.add(designer)
    
    db.session.commit()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

