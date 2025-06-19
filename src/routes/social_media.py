from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.social_media import SocialMedia
from datetime import datetime

social_media_bp = Blueprint('social_media', __name__)

@social_media_bp.route('/social-media', methods=['GET'])
def get_social_medias():
    try:
        social_medias = SocialMedia.query.all()
        return jsonify([sm.to_dict() for sm in social_medias])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@social_media_bp.route('/social-media/<int:sm_id>', methods=['GET'])
def get_social_media(sm_id):
    try:
        social_media = SocialMedia.query.get_or_404(sm_id)
        return jsonify(social_media.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@social_media_bp.route('/social-media', methods=['POST'])
def create_social_media():
    try:
        data = request.get_json()
        
        social_media = SocialMedia(
            cliente_id=data['cliente_id'],
            tipo_conteudo=data.get('tipo_conteudo'),
            tema_titulo=data.get('tema_titulo'),
            briefing=data.get('briefing'),
            status=data.get('status', 'pendente'),
            data_publicacao=datetime.fromisoformat(data['data_publicacao']) if data.get('data_publicacao') else None,
            link_arte=data.get('link_arte'),
            responsavel_id=data.get('responsavel_id'),
            observacoes=data.get('observacoes')
        )
        
        db.session.add(social_media)
        db.session.commit()
        
        return jsonify(social_media.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@social_media_bp.route('/social-media/<int:sm_id>', methods=['PUT'])
def update_social_media(sm_id):
    try:
        social_media = SocialMedia.query.get_or_404(sm_id)
        data = request.get_json()
        
        social_media.cliente_id = data.get('cliente_id', social_media.cliente_id)
        social_media.tipo_conteudo = data.get('tipo_conteudo', social_media.tipo_conteudo)
        social_media.tema_titulo = data.get('tema_titulo', social_media.tema_titulo)
        social_media.briefing = data.get('briefing', social_media.briefing)
        social_media.status = data.get('status', social_media.status)
        social_media.data_publicacao = datetime.fromisoformat(data['data_publicacao']) if data.get('data_publicacao') else social_media.data_publicacao
        social_media.link_arte = data.get('link_arte', social_media.link_arte)
        social_media.responsavel_id = data.get('responsavel_id', social_media.responsavel_id)
        social_media.observacoes = data.get('observacoes', social_media.observacoes)
        social_media.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify(social_media.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@social_media_bp.route('/social-media/<int:sm_id>', methods=['DELETE'])
def delete_social_media(sm_id):
    try:
        social_media = SocialMedia.query.get_or_404(sm_id)
        db.session.delete(social_media)
        db.session.commit()
        
        return jsonify({'message': 'Social Media deletado com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

