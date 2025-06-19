from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.automacao import Automacao
from datetime import datetime

automacao_bp = Blueprint('automacao', __name__)

@automacao_bp.route('/automacoes', methods=['GET'])
def get_automacoes():
    try:
        automacoes = Automacao.query.all()
        return jsonify([automacao.to_dict() for automacao in automacoes])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@automacao_bp.route('/automacoes/<int:automacao_id>', methods=['GET'])
def get_automacao(automacao_id):
    try:
        automacao = Automacao.query.get_or_404(automacao_id)
        return jsonify(automacao.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@automacao_bp.route('/automacoes', methods=['POST'])
def create_automacao():
    try:
        data = request.get_json()
        
        automacao = Automacao(
            cliente_id=data['cliente_id'],
            tipo_automacao=data.get('tipo_automacao'),
            nome_projeto=data['nome_projeto'],
            escopo=data.get('escopo'),
            status=data.get('status', 'planejamento'),
            responsavel_tecnico_id=data.get('responsavel_tecnico_id'),
            complexidade=data.get('complexidade', 'media'),
            prazo=datetime.fromisoformat(data['prazo']) if data.get('prazo') else None,
            link_fluxo=data.get('link_fluxo'),
            webhook_url=data.get('webhook_url'),
            api_keys=data.get('api_keys'),
            observacoes_tecnicas=data.get('observacoes_tecnicas')
        )
        
        db.session.add(automacao)
        db.session.commit()
        
        return jsonify(automacao.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@automacao_bp.route('/automacoes/<int:automacao_id>', methods=['PUT'])
def update_automacao(automacao_id):
    try:
        automacao = Automacao.query.get_or_404(automacao_id)
        data = request.get_json()
        
        automacao.cliente_id = data.get('cliente_id', automacao.cliente_id)
        automacao.tipo_automacao = data.get('tipo_automacao', automacao.tipo_automacao)
        automacao.nome_projeto = data.get('nome_projeto', automacao.nome_projeto)
        automacao.escopo = data.get('escopo', automacao.escopo)
        automacao.status = data.get('status', automacao.status)
        automacao.responsavel_tecnico_id = data.get('responsavel_tecnico_id', automacao.responsavel_tecnico_id)
        automacao.complexidade = data.get('complexidade', automacao.complexidade)
        automacao.prazo = datetime.fromisoformat(data['prazo']) if data.get('prazo') else automacao.prazo
        automacao.link_fluxo = data.get('link_fluxo', automacao.link_fluxo)
        automacao.webhook_url = data.get('webhook_url', automacao.webhook_url)
        automacao.api_keys = data.get('api_keys', automacao.api_keys)
        automacao.observacoes_tecnicas = data.get('observacoes_tecnicas', automacao.observacoes_tecnicas)
        automacao.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify(automacao.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@automacao_bp.route('/automacoes/<int:automacao_id>', methods=['DELETE'])
def delete_automacao(automacao_id):
    try:
        automacao = Automacao.query.get_or_404(automacao_id)
        db.session.delete(automacao)
        db.session.commit()
        
        return jsonify({'message': 'Automação deletada com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

