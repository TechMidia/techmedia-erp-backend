from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.financeiro import Financeiro
from sqlalchemy import func, extract
from datetime import datetime

financeiro_bp = Blueprint('financeiro', __name__)

@financeiro_bp.route('/financeiro', methods=['GET'])
def get_financeiro():
    try:
        financeiros = Financeiro.query.all()
        return jsonify([financeiro.to_dict() for financeiro in financeiros])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@financeiro_bp.route('/financeiro/<int:financeiro_id>', methods=['GET'])
def get_financeiro_item(financeiro_id):
    try:
        financeiro = Financeiro.query.get_or_404(financeiro_id)
        return jsonify(financeiro.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@financeiro_bp.route('/financeiro', methods=['POST'])
def create_financeiro():
    try:
        data = request.get_json()
        
        financeiro = Financeiro(
            tipo_registro=data['tipo_registro'],
            cliente_fornecedor=data.get('cliente_fornecedor'),
            pedido_id=data.get('pedido_id'),
            valor=data['valor'],
            custo=data.get('custo', 0),
            status=data.get('status', 'pendente'),
            categoria=data.get('categoria'),
            forma_pagamento=data.get('forma_pagamento'),
            data_vencimento=datetime.fromisoformat(data['data_vencimento']) if data.get('data_vencimento') else None,
            data_pagamento=datetime.fromisoformat(data['data_pagamento']) if data.get('data_pagamento') else None,
            referencia_mensal=data.get('referencia_mensal', datetime.now().strftime('%Y-%m')),
            observacoes=data.get('observacoes')
        )
        
        financeiro.calculate_lucro()
        
        db.session.add(financeiro)
        db.session.commit()
        
        return jsonify(financeiro.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@financeiro_bp.route('/financeiro/<int:financeiro_id>', methods=['PUT'])
def update_financeiro(financeiro_id):
    try:
        financeiro = Financeiro.query.get_or_404(financeiro_id)
        data = request.get_json()
        
        financeiro.tipo_registro = data.get('tipo_registro', financeiro.tipo_registro)
        financeiro.cliente_fornecedor = data.get('cliente_fornecedor', financeiro.cliente_fornecedor)
        financeiro.pedido_id = data.get('pedido_id', financeiro.pedido_id)
        financeiro.valor = data.get('valor', financeiro.valor)
        financeiro.custo = data.get('custo', financeiro.custo)
        financeiro.status = data.get('status', financeiro.status)
        financeiro.categoria = data.get('categoria', financeiro.categoria)
        financeiro.forma_pagamento = data.get('forma_pagamento', financeiro.forma_pagamento)
        financeiro.data_vencimento = datetime.fromisoformat(data['data_vencimento']) if data.get('data_vencimento') else financeiro.data_vencimento
        financeiro.data_pagamento = datetime.fromisoformat(data['data_pagamento']) if data.get('data_pagamento') else financeiro.data_pagamento
        financeiro.referencia_mensal = data.get('referencia_mensal', financeiro.referencia_mensal)
        financeiro.observacoes = data.get('observacoes', financeiro.observacoes)
        financeiro.updated_at = datetime.utcnow()
        
        financeiro.calculate_lucro()
        
        db.session.commit()
        
        return jsonify(financeiro.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@financeiro_bp.route('/financeiro/kpis', methods=['GET'])
def get_kpis_financeiro():
    try:
        mes_atual = datetime.now().strftime('%Y-%m')
        
        # Receitas do mês
        receitas = db.session.query(func.sum(Financeiro.valor)).filter(
            Financeiro.tipo_registro == 'receita',
            Financeiro.referencia_mensal == mes_atual
        ).scalar() or 0
        
        # Custos do mês
        custos = db.session.query(func.sum(Financeiro.valor)).filter(
            Financeiro.tipo_registro.in_(['despesa_variavel', 'custo_fixo']),
            Financeiro.referencia_mensal == mes_atual
        ).scalar() or 0
        
        # Lucro do mês
        lucro = db.session.query(func.sum(Financeiro.lucro)).filter(
            Financeiro.referencia_mensal == mes_atual
        ).scalar() or 0
        
        # Contas a receber
        contas_receber = db.session.query(func.sum(Financeiro.valor)).filter(
            Financeiro.tipo_registro == 'receita',
            Financeiro.status == 'pendente'
        ).scalar() or 0
        
        # Contas a pagar
        contas_pagar = db.session.query(func.sum(Financeiro.valor)).filter(
            Financeiro.tipo_registro.in_(['despesa_variavel', 'custo_fixo']),
            Financeiro.status == 'pendente'
        ).scalar() or 0
        
        return jsonify({
            'receitas_mes': receitas,
            'custos_mes': custos,
            'lucro_mes': lucro,
            'contas_receber': contas_receber,
            'contas_pagar': contas_pagar
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@financeiro_bp.route('/financeiro/<int:financeiro_id>', methods=['DELETE'])
def delete_financeiro(financeiro_id):
    try:
        financeiro = Financeiro.query.get_or_404(financeiro_id)
        db.session.delete(financeiro)
        db.session.commit()
        
        return jsonify({'message': 'Registro financeiro deletado com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

