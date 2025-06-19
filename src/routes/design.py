from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.design import Design
from datetime import datetime

design_bp = Blueprint('design', __name__)

@design_bp.route('/designs', methods=['GET'])
def get_designs():
    try:
        designs = Design.query.all()
        return jsonify([design.to_dict() for design in designs])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@design_bp.route('/designs/<int:design_id>', methods=['GET'])
def get_design(design_id):
    try:
        design = Design.query.get_or_404(design_id)
        return jsonify(design.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@design_bp.route('/designs', methods=['POST'])
def create_design():
    try:
        data = request.get_json()
        
        design = Design(
            tipo_arte=data.get('tipo_arte'),
            cliente_id=data['cliente_id'],
            pedido_id=data.get('pedido_id'),
            status=data.get('status', 'pendente'),
            responsavel_id=data.get('responsavel_id'),
            link_arte=data.get('link_arte'),
            prazo=datetime.fromisoformat(data['prazo']) if data.get('prazo') else None,
            observacoes=data.get('observacoes'),
            briefing_criativo=data.get('briefing_criativo'),
            revisoes=data.get('revisoes', 0)
        )
        
        db.session.add(design)
        db.session.commit()
        
        return jsonify(design.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@design_bp.route('/designs/<int:design_id>', methods=['PUT'])
def update_design(design_id):
    try:
        design = Design.query.get_or_404(design_id)
        data = request.get_json()
        
        design.tipo_arte = data.get('tipo_arte', design.tipo_arte)
        design.cliente_id = data.get('cliente_id', design.cliente_id)
        design.pedido_id = data.get('pedido_id', design.pedido_id)
        design.status = data.get('status', design.status)
        design.responsavel_id = data.get('responsavel_id', design.responsavel_id)
        design.link_arte = data.get('link_arte', design.link_arte)
        design.prazo = datetime.fromisoformat(data['prazo']) if data.get('prazo') else design.prazo
        design.observacoes = data.get('observacoes', design.observacoes)
        design.briefing_criativo = data.get('briefing_criativo', design.briefing_criativo)
        design.revisoes = data.get('revisoes', design.revisoes)
        design.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify(design.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@design_bp.route('/designs/<int:design_id>', methods=['DELETE'])
def delete_design(design_id):
    try:
        design = Design.query.get_or_404(design_id)
        db.session.delete(design)
        db.session.commit()
        
        return jsonify({'message': 'Design deletado com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

