from flask import Blueprint, request, jsonify
from src.models.user import db, User
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import jwt
import os

user_bp = Blueprint('user', __name__)

# Chave secreta para JWT (em produção, use uma variável de ambiente)
JWT_SECRET = os.environ.get('JWT_SECRET', 'techmedia_erp_secret_key')

@user_bp.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username e password são obrigatórios'}), 400
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            return jsonify({'error': 'Credenciais inválidas'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Usuário inativo'}), 401
        
        # Atualizar último login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Gerar token JWT
        token_payload = {
            'user_id': user.id,
            'username': user.username,
            'role': user.role,
            'exp': datetime.utcnow().timestamp() + 86400  # 24 horas
        }
        
        token = jwt.encode(token_payload, JWT_SECRET, algorithm='HS256')
        
        return jsonify({
            'token': token,
            'user': user.to_dict()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/auth/verify', methods=['POST'])
def verify_token():
    try:
        data = request.get_json()
        token = data.get('token')
        
        if not token:
            return jsonify({'error': 'Token não fornecido'}), 400
        
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            user = User.query.get(payload['user_id'])
            
            if not user or not user.is_active:
                return jsonify({'error': 'Usuário inválido'}), 401
            
            return jsonify({
                'valid': True,
                'user': user.to_dict()
            })
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        return jsonify(user.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        
        # Verificar se username já existe
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username já existe'}), 400
        
        # Verificar se email já existe
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email já existe'}), 400
        
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=generate_password_hash(data['password']),
            role=data.get('role', 'designer'),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify(user.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        # Verificar se novo username já existe (se foi alterado)
        if 'username' in data and data['username'] != user.username:
            if User.query.filter_by(username=data['username']).first():
                return jsonify({'error': 'Username já existe'}), 400
        
        # Verificar se novo email já existe (se foi alterado)
        if 'email' in data and data['email'] != user.email:
            if User.query.filter_by(email=data['email']).first():
                return jsonify({'error': 'Email já existe'}), 400
        
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.role = data.get('role', user.role)
        user.is_active = data.get('is_active', user.is_active)
        
        # Atualizar senha se fornecida
        if 'password' in data and data['password']:
            user.password_hash = generate_password_hash(data['password'])
        
        db.session.commit()
        
        return jsonify(user.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        
        # Não permitir deletar o próprio usuário (implementar verificação de token se necessário)
        # Por segurança, apenas desativar ao invés de deletar
        user.is_active = False
        db.session.commit()
        
        return jsonify({'message': 'Usuário desativado com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<int:user_id>/change-password', methods=['POST'])
def change_password(user_id):
    try:
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return jsonify({'error': 'Senha atual e nova senha são obrigatórias'}), 400
        
        if not user.check_password(current_password):
            return jsonify({'error': 'Senha atual incorreta'}), 400
        
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        
        return jsonify({'message': 'Senha alterada com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

