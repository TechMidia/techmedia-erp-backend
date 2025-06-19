from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.grafica import Grafica
from datetime import datetime

grafica_bp = Blueprint('grafica', __name__)

@grafica_bp.route('/graficas', methods=['GET'])
def get_graficas():
    try:
        graficas = Grafica.query.all()
        return jsonify([grafica.to_dict() for grafica in graficas])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@grafica_bp.route('/graficas/<int:grafica_id>', methods=['GET'])
def get_grafica(grafica_id):
    try:
        grafica = Grafica.query.get_or_404(grafica_id)
        return jsonify(grafica.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@grafica_bp.route('/graficas', methods=['POST'])
def create_grafica():
    try:
        data = request.get_json()
        
        grafica = Grafica(
            produto=data['produto'],
            categoria=data.get('categoria'),
            cliente_id=data['cliente_id'],
            pedido_id=data.get('pedido_id'),
            fornecedor_id=data.get('fornecedor_id'),
            custo_unitario=data['custo_unitario'],
            quantidade=data['quantidade'],
            preco_venda=data['preco_venda'],
            prazo=datetime.fromisoformat(data['prazo']) if data.get('prazo') else None,
            status=data.get('status', 'orcamento'),
            link_arte=data.get('link_arte'),
            observacoes=data.get('observacoes')
        )
        
        grafica.calculate_custo_total()
        
        db.session.add(grafica)
        db.session.commit()
        
        return jsonify(grafica.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@grafica_bp.route('/graficas/<int:grafica_id>', methods=['PUT'])
def update_grafica(grafica_id):
    try:
        grafica = Grafica.query.get_or_404(grafica_id)
        data = request.get_json()
        
        grafica.produto = data.get('produto', grafica.produto)
        grafica.categoria = data.get('categoria', grafica.categoria)
        grafica.cliente_id = data.get('cliente_id', grafica.cliente_id)
        grafica.pedido_id = data.get('pedido_id', grafica.pedido_id)
        grafica.fornecedor_id = data.get('fornecedor_id', grafica.fornecedor_id)
        grafica.custo_unitario = data.get('custo_unitario', grafica.custo_unitario)
        grafica.quantidade = data.get('quantidade', grafica.quantidade)
        grafica.preco_venda = data.get('preco_venda', grafica.preco_venda)
        grafica.prazo = datetime.fromisoformat(data['prazo']) if data.get('prazo') else grafica.prazo
        grafica.status = data.get('status', grafica.status)
        grafica.link_arte = data.get('link_arte', grafica.link_arte)
        grafica.observacoes = data.get('observacoes', grafica.observacoes)
        grafica.updated_at = datetime.utcnow()
        
        grafica.calculate_custo_total()
        
        db.session.commit()
        
        return jsonify(grafica.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@grafica_bp.route('/graficas/<int:grafica_id>', methods=['DELETE'])
def delete_grafica(grafica_id):
    try:
        grafica = Grafica.query.get_or_404(grafica_id)
        db.session.delete(grafica)
        db.session.commit()
        
        return jsonify({'message': 'Gráfica deletada com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

