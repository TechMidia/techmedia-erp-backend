from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.pedido import Pedido
from src.models.financeiro import Financeiro
from src.models.tarefa import Tarefa
from datetime import datetime

pedido_bp = Blueprint('pedido', __name__)

@pedido_bp.route('/pedidos', methods=['GET'])
def get_pedidos():
    try:
        pedidos = Pedido.query.all()
        return jsonify([pedido.to_dict() for pedido in pedidos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pedido_bp.route('/pedidos/<int:pedido_id>', methods=['GET'])
def get_pedido(pedido_id):
    try:
        pedido = Pedido.query.get_or_404(pedido_id)
        return jsonify(pedido.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pedido_bp.route('/pedidos', methods=['POST'])
def create_pedido():
    try:
        data = request.get_json()
        
        # Gerar código único
        ultimo_pedido = Pedido.query.order_by(Pedido.id.desc()).first()
        proximo_numero = (ultimo_pedido.id + 1) if ultimo_pedido else 1
        codigo = f"PED{proximo_numero:03d}"
        
        pedido = Pedido(
            codigo=codigo,
            cliente_id=data['cliente_id'],
            servico_id=data['servico_id'],
            categoria=data.get('categoria'),
            deadline=datetime.fromisoformat(data['deadline']) if data.get('deadline') else None,
            status=data.get('status', 'pendente'),
            responsavel_id=data.get('responsavel_id'),
            valor=data['valor'],
            link_arquivo=data.get('link_arquivo'),
            observacoes=data.get('observacoes'),
            briefing=data.get('briefing')
        )
        
        db.session.add(pedido)
        db.session.flush()  # Para obter o ID do pedido
        
        # Criar entrada financeira automaticamente
        financeiro = Financeiro(
            tipo_registro='receita',
            cliente_fornecedor=pedido.cliente.nome,
            pedido_id=pedido.id,
            valor=pedido.valor,
            custo=pedido.servico.custo if pedido.servico else 0,
            status='pendente',
            categoria=pedido.categoria,
            referencia_mensal=datetime.now().strftime('%Y-%m')
        )
        financeiro.calculate_lucro()
        db.session.add(financeiro)
        
        # Criar tarefa automaticamente se for design
        if pedido.categoria and 'design' in pedido.categoria.lower():
            tarefa = Tarefa(
                titulo=f"Criar {pedido.categoria} - {pedido.cliente.nome}",
                descricao=f"Pedido: {pedido.codigo}",
                responsavel_id=pedido.responsavel_id,
                area_relacionada='design',
                pedido_id=pedido.id,
                cliente_id=pedido.cliente_id,
                data_entrega=pedido.deadline,
                prioridade='media'
            )
            db.session.add(tarefa)
        
        db.session.commit()
        
        return jsonify(pedido.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@pedido_bp.route('/pedidos/<int:pedido_id>', methods=['PUT'])
def update_pedido(pedido_id):
    try:
        pedido = Pedido.query.get_or_404(pedido_id)
        data = request.get_json()
        
        pedido.cliente_id = data.get('cliente_id', pedido.cliente_id)
        pedido.servico_id = data.get('servico_id', pedido.servico_id)
        pedido.categoria = data.get('categoria', pedido.categoria)
        pedido.deadline = datetime.fromisoformat(data['deadline']) if data.get('deadline') else pedido.deadline
        pedido.status = data.get('status', pedido.status)
        pedido.responsavel_id = data.get('responsavel_id', pedido.responsavel_id)
        pedido.valor = data.get('valor', pedido.valor)
        pedido.link_arquivo = data.get('link_arquivo', pedido.link_arquivo)
        pedido.observacoes = data.get('observacoes', pedido.observacoes)
        pedido.briefing = data.get('briefing', pedido.briefing)
        pedido.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify(pedido.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@pedido_bp.route('/pedidos/<int:pedido_id>', methods=['DELETE'])
def delete_pedido(pedido_id):
    try:
        pedido = Pedido.query.get_or_404(pedido_id)
        db.session.delete(pedido)
        db.session.commit()
        
        return jsonify({'message': 'Pedido deletado com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

