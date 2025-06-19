from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.servico import Servico
from datetime import datetime

servico_bp = Blueprint('servico', __name__)

@servico_bp.route('/servicos', methods=['GET'])
def get_servicos():
    try:
        servicos = Servico.query.all()
        return jsonify([servico.to_dict() for servico in servicos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@servico_bp.route('/servicos/<int:servico_id>', methods=['GET'])
def get_servico(servico_id):
    try:
        servico = Servico.query.get_or_404(servico_id)
        return jsonify(servico.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@servico_bp.route('/servicos', methods=['POST'])
def create_servico():
    try:
        data = request.get_json()
        
        servico = Servico(
            nome=data['nome'],
            categoria=data.get('categoria'),
            descricao=data.get('descricao'),
            preco=data['preco'],
            custo=data.get('custo', 0),
            tempo_entrega=data.get('tempo_entrega'),
            is_recorrente=data.get('is_recorrente', False),
            fornecedor_externo=data.get('fornecedor_externo', False),
            fornecedor_id=data.get('fornecedor_id'),
            link_fornecedor=data.get('link_fornecedor'),
            status=data.get('status', 'ativo')
        )
        
        db.session.add(servico)
        db.session.commit()
        
        return jsonify(servico.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@servico_bp.route('/servicos/<int:servico_id>', methods=['PUT'])
def update_servico(servico_id):
    try:
        servico = Servico.query.get_or_404(servico_id)
        data = request.get_json()
        
        servico.nome = data.get('nome', servico.nome)
        servico.categoria = data.get('categoria', servico.categoria)
        servico.descricao = data.get('descricao', servico.descricao)
        servico.preco = data.get('preco', servico.preco)
        servico.custo = data.get('custo', servico.custo)
        servico.tempo_entrega = data.get('tempo_entrega', servico.tempo_entrega)
        servico.is_recorrente = data.get('is_recorrente', servico.is_recorrente)
        servico.fornecedor_externo = data.get('fornecedor_externo', servico.fornecedor_externo)
        servico.fornecedor_id = data.get('fornecedor_id', servico.fornecedor_id)
        servico.link_fornecedor = data.get('link_fornecedor', servico.link_fornecedor)
        servico.status = data.get('status', servico.status)
        servico.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify(servico.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@servico_bp.route('/servicos/<int:servico_id>', methods=['DELETE'])
def delete_servico(servico_id):
    try:
        servico = Servico.query.get_or_404(servico_id)
        db.session.delete(servico)
        db.session.commit()
        
        return jsonify({'message': 'Serviço deletado com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

