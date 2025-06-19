from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.fornecedor import Fornecedor
from datetime import datetime

fornecedor_bp = Blueprint('fornecedor', __name__)

@fornecedor_bp.route('/fornecedores', methods=['GET'])
def get_fornecedores():
    try:
        fornecedores = Fornecedor.query.all()
        return jsonify([fornecedor.to_dict() for fornecedor in fornecedores])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@fornecedor_bp.route('/fornecedores/<int:fornecedor_id>', methods=['GET'])
def get_fornecedor(fornecedor_id):
    try:
        fornecedor = Fornecedor.query.get_or_404(fornecedor_id)
        return jsonify(fornecedor.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@fornecedor_bp.route('/fornecedores', methods=['POST'])
def create_fornecedor():
    try:
        data = request.get_json()
        
        fornecedor = Fornecedor(
            nome=data['nome'],
            categoria=data.get('categoria'),
            contato=data.get('contato'),
            telefone=data.get('telefone'),
            email=data.get('email'),
            endereco=data.get('endereco'),
            tabela_preco_link=data.get('tabela_preco_link'),
            api_disponivel=data.get('api_disponivel', False),
            api_endpoint=data.get('api_endpoint'),
            api_key=data.get('api_key'),
            site=data.get('site'),
            status=data.get('status', 'ativo'),
            observacoes=data.get('observacoes')
        )
        
        db.session.add(fornecedor)
        db.session.commit()
        
        return jsonify(fornecedor.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@fornecedor_bp.route('/fornecedores/<int:fornecedor_id>', methods=['PUT'])
def update_fornecedor(fornecedor_id):
    try:
        fornecedor = Fornecedor.query.get_or_404(fornecedor_id)
        data = request.get_json()
        
        fornecedor.nome = data.get('nome', fornecedor.nome)
        fornecedor.categoria = data.get('categoria', fornecedor.categoria)
        fornecedor.contato = data.get('contato', fornecedor.contato)
        fornecedor.telefone = data.get('telefone', fornecedor.telefone)
        fornecedor.email = data.get('email', fornecedor.email)
        fornecedor.endereco = data.get('endereco', fornecedor.endereco)
        fornecedor.tabela_preco_link = data.get('tabela_preco_link', fornecedor.tabela_preco_link)
        fornecedor.api_disponivel = data.get('api_disponivel', fornecedor.api_disponivel)
        fornecedor.api_endpoint = data.get('api_endpoint', fornecedor.api_endpoint)
        fornecedor.api_key = data.get('api_key', fornecedor.api_key)
        fornecedor.site = data.get('site', fornecedor.site)
        fornecedor.status = data.get('status', fornecedor.status)
        fornecedor.observacoes = data.get('observacoes', fornecedor.observacoes)
        fornecedor.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify(fornecedor.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@fornecedor_bp.route('/fornecedores/<int:fornecedor_id>', methods=['DELETE'])
def delete_fornecedor(fornecedor_id):
    try:
        fornecedor = Fornecedor.query.get_or_404(fornecedor_id)
        db.session.delete(fornecedor)
        db.session.commit()
        
        return jsonify({'message': 'Fornecedor deletado com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

