from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.tarefa import Tarefa
from datetime import datetime

tarefa_bp = Blueprint('tarefa', __name__)

@tarefa_bp.route('/tarefas', methods=['GET'])
def get_tarefas():
    try:
        tarefas = Tarefa.query.all()
        return jsonify([tarefa.to_dict() for tarefa in tarefas])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tarefa_bp.route('/tarefas/<int:tarefa_id>', methods=['GET'])
def get_tarefa(tarefa_id):
    try:
        tarefa = Tarefa.query.get_or_404(tarefa_id)
        return jsonify(tarefa.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tarefa_bp.route('/tarefas', methods=['POST'])
def create_tarefa():
    try:
        data = request.get_json()
        
        tarefa = Tarefa(
            titulo=data['titulo'],
            descricao=data.get('descricao'),
            responsavel_id=data['responsavel_id'],
            area_relacionada=data.get('area_relacionada'),
            pedido_id=data.get('pedido_id'),
            cliente_id=data.get('cliente_id'),
            data_entrega=datetime.fromisoformat(data['data_entrega']) if data.get('data_entrega') else None,
            prioridade=data.get('prioridade', 'media'),
            status=data.get('status', 'pendente'),
            progresso=data.get('progresso', 0),
            tempo_estimado=data.get('tempo_estimado'),
            tempo_gasto=data.get('tempo_gasto', 0),
            observacoes=data.get('observacoes')
        )
        
        db.session.add(tarefa)
        db.session.commit()
        
        return jsonify(tarefa.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@tarefa_bp.route('/tarefas/<int:tarefa_id>', methods=['PUT'])
def update_tarefa(tarefa_id):
    try:
        tarefa = Tarefa.query.get_or_404(tarefa_id)
        data = request.get_json()
        
        tarefa.titulo = data.get('titulo', tarefa.titulo)
        tarefa.descricao = data.get('descricao', tarefa.descricao)
        tarefa.responsavel_id = data.get('responsavel_id', tarefa.responsavel_id)
        tarefa.area_relacionada = data.get('area_relacionada', tarefa.area_relacionada)
        tarefa.pedido_id = data.get('pedido_id', tarefa.pedido_id)
        tarefa.cliente_id = data.get('cliente_id', tarefa.cliente_id)
        tarefa.data_entrega = datetime.fromisoformat(data['data_entrega']) if data.get('data_entrega') else tarefa.data_entrega
        tarefa.prioridade = data.get('prioridade', tarefa.prioridade)
        tarefa.status = data.get('status', tarefa.status)
        tarefa.progresso = data.get('progresso', tarefa.progresso)
        tarefa.tempo_estimado = data.get('tempo_estimado', tarefa.tempo_estimado)
        tarefa.tempo_gasto = data.get('tempo_gasto', tarefa.tempo_gasto)
        tarefa.observacoes = data.get('observacoes', tarefa.observacoes)
        tarefa.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify(tarefa.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@tarefa_bp.route('/tarefas/<int:tarefa_id>', methods=['DELETE'])
def delete_tarefa(tarefa_id):
    try:
        tarefa = Tarefa.query.get_or_404(tarefa_id)
        db.session.delete(tarefa)
        db.session.commit()
        
        return jsonify({'message': 'Tarefa deletada com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

