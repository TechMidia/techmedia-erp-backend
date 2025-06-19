from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.cliente import Cliente
from datetime import datetime

cliente_bp = Blueprint('cliente', __name__)

@cliente_bp.route('/clientes', methods=['GET'])
def get_clientes():
    try:
        clientes = Cliente.query.all()
        return jsonify([cliente.to_dict() for cliente in clientes])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cliente_bp.route('/clientes/<int:cliente_id>', methods=['GET'])
def get_cliente(cliente_id):
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        return jsonify(cliente.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cliente_bp.route('/clientes', methods=['POST'])
def create_cliente():
    try:
        data = request.get_json()
        
        # Gerar código único
        ultimo_cliente = Cliente.query.order_by(Cliente.id.desc()).first()
        proximo_numero = (ultimo_cliente.id + 1) if ultimo_cliente else 1
        codigo = f"CLI{proximo_numero:03d}"
        
        cliente = Cliente(
            codigo=codigo,
            nome=data['nome'],
            cpf_cnpj=data.get('cpf_cnpj'),
            cidade=data.get('cidade'),
            estado=data.get('estado'),
            tipo=data.get('tipo'),
            forma_pagamento=data.get('forma_pagamento'),
            status=data.get('status', 'ativo'),
            responsavel_interno_id=data.get('responsavel_interno_id'),
            observacoes=data.get('observacoes')
        )
        
        db.session.add(cliente)
        db.session.commit()
        
        return jsonify(cliente.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cliente_bp.route('/clientes/<int:cliente_id>', methods=['PUT'])
def update_cliente(cliente_id):
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        data = request.get_json()
        
        cliente.nome = data.get('nome', cliente.nome)
        cliente.cpf_cnpj = data.get('cpf_cnpj', cliente.cpf_cnpj)
        cliente.cidade = data.get('cidade', cliente.cidade)
        cliente.estado = data.get('estado', cliente.estado)
        cliente.tipo = data.get('tipo', cliente.tipo)
        cliente.forma_pagamento = data.get('forma_pagamento', cliente.forma_pagamento)
        cliente.status = data.get('status', cliente.status)
        cliente.responsavel_interno_id = data.get('responsavel_interno_id', cliente.responsavel_interno_id)
        cliente.observacoes = data.get('observacoes', cliente.observacoes)
        cliente.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify(cliente.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cliente_bp.route('/clientes/<int:cliente_id>', methods=['DELETE'])
def delete_cliente(cliente_id):
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        db.session.delete(cliente)
        db.session.commit()
        
        return jsonify({'message': 'Cliente deletado com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

